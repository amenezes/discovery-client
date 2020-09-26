import asyncio
import json
import pickle

from discovery import log
from discovery.abc import BaseClient
from discovery.exceptions import NoConsulLeaderException, ServiceNotFoundException
from discovery.model.agent.service import service
from discovery.utils import select_one_rr


class Consul(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.managed_services = {}
        self._leader_id = None
        self.consul_current_leader_id = None

    async def find_service(self, name, fn=select_one_rr):
        response = await self.find_services(name)
        try:
            return fn(response)
        except Exception:
            raise ServiceNotFoundException(
                f"service {name} not found in the Consul's catalog"
            )

    async def find_services(self, name):
        resp = await self.catalog.service(name)
        response = await self._get_response(resp)
        return response

    async def register(
        self, service_name: str, service_port: int, check=None, dump_service=True
    ) -> None:
        svc = service(service_name, service_port, check=check)
        try:
            await self.agent.service.register(svc)
            self.managed_services[json.loads(svc).get("id")] = {
                "service_name": service_name,
                "port": service_port,
                "check": check,
            }
            self.consul_current_leader_id = await self.leader_current_id()
            if dump_service:
                self._dump_registered_service
        except Exception as err:
            raise err

    def _dump_registered_service(self):
        with open(".service", "wb") as f:
            f.write(pickle.dumps(self.managed_services))

    async def check_consul_health(self):
        while True:
            try:
                await asyncio.sleep(self.timeout)
                current_id = await self.leader_current_id()
                if current_id != self.consul_current_leader_id:
                    await self.reconnect()
            except Exception:
                await asyncio.sleep(self.timeout)
                await self.check_consul_health()

    async def reconnect(self):
        old_service = self.managed_services.copy()
        await self.deregister()
        for key, value in old_service.items():
            await self.register(
                service_name=value.get("service_name"),
                service_port=value.get("port"),
                check=value.get("check"),
            )
        log.info("Service successfully re-registered")

    async def leader_current_id(self):
        consul_leader = await self.leader_ip()
        consul_instances = await self.consul_healthy_instances()

        current_id = [
            instance.get("Node").get("ID")
            for instance in consul_instances
            if instance.get("Node").get("Address") == consul_leader
        ]
        if current_id is not None:
            current_id = current_id[0]
        return current_id

    async def leader_ip(self):
        leader_response = await self.status.leader()
        leader_response = await self._get_response(leader_response)
        try:
            consul_leader, _ = leader_response.split(":")
        except ValueError:
            raise NoConsulLeaderException("Error to identify Consul's leader.")
        return consul_leader

    async def consul_healthy_instances(self):
        health_response = await self.health.service("consul")
        consul_instances = await self._get_response(health_response)
        return consul_instances

    async def _get_response(self, resp):
        try:
            response = await resp.json()
            return response
        except Exception:
            response = await resp.text()
            return response

    async def deregister(self) -> None:
        for service_id in self.managed_services.keys():
            await self.agent.service.deregister(service_id)
        self.managed_services.clear()
