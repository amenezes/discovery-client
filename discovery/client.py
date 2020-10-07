import asyncio
import json
import os
import pickle

from discovery import api, utils
from discovery.engine.aiohttp import AIOHTTPEngine
from discovery.exceptions import NoConsulLeaderException


class Consul:
    def __init__(self, client=None, *args, **kwargs):
        self.client = client or AIOHTTPEngine(*args, **kwargs)
        self.catalog = api.Catalog(client=self.client)
        self.config = api.Config(client=self.client)
        self.coordinate = api.Coordinate(client=self.client)
        self.events = api.Events(client=self.client)
        self.health = api.Health(client=self.client)
        self.kv = api.Kv(client=self.client)
        self.query = api.Query(client=self.client)
        self.session = api.Session(client=self.client)
        self.snapshot = api.Snapshot(client=self.client)
        self.status = api.Status(client=self.client)
        self.txn = api.Txn(client=self.client)
        self.agent = api.Agent(client=self.client)
        self.connect = api.Connect(client=self.client)
        self.acl = api.Acl(client=self.client)
        self.operator = api.Operator(client=self.client)
        self.timeout = int(os.getenv("DEFAULT_TIMEOUT", 30))
        self.leader_active_id = None

    async def leader_ip(self):
        response = await self.status.leader()
        try:
            current_leader = await response.json()
            leader_ip, _ = current_leader.split(":")
        except Exception:
            raise NoConsulLeaderException("Error to identify Consul's leader.")
        return leader_ip

    async def leader_id(self):
        consul_leader_ip = await self.leader_ip()
        consul_health_instances = await self.health.service("consul")
        consul_health_instances = await consul_health_instances.json()
        current_id = [
            instance["Node"]["ID"]
            for instance in consul_health_instances
            if instance["Node"]["Address"] == consul_leader_ip
        ]
        try:
            return current_id[0]
        except Exception:
            raise NoConsulLeaderException

    async def find_services(self, name: str):
        response = await self.catalog.service(name)
        response = await response.json()
        return response

    async def find_service(self, name: str, fn=utils.select_one_rr):
        response = await self.find_services(name)
        return fn(response)

    async def register(self, service, dump_service=True):
        try:
            await self.agent.service.register(service)
            self.leader_active_id = await self.leader_id()
            if dump_service:
                with open(".service", "wb") as f:
                    f.write(pickle.dumps(service))
        except Exception as err:
            raise err

    async def deregister(self, service):
        service_id = json.loads(service)["id"]
        await self.agent.service.deregister(service_id)

    async def reconnect(self, service):
        await self.deregister(service)
        await self.register(service)

    async def watch_connection(self, service):
        while True:
            try:
                await asyncio.sleep(self.timeout)
                await self._remove_duplicate_services(service)
                current_id = await self.leader_id()
                if current_id != self.leader_active_id:
                    await self.reconnect(service)
            except Exception:
                await asyncio.sleep(self.timeout)
                await self.watch_connection(service)

    async def _remove_duplicate_services(self, service):
        current_service = json.loads(service)
        resp = await self.find_services(current_service["name"])
        duplicate = [
            self.deregister(
                utils.service(
                    name=registered_service["ServiceName"],
                    port=registered_service["ServicePort"],
                    service_id=registered_service["ServiceID"],
                )
            )
            for registered_service in resp
            if (registered_service["ServiceAddress"] == current_service["address"])
            and (registered_service["ServiceID"] != current_service["id"])
        ]
        await asyncio.gather(*duplicate)

    def __repr__(self):
        return f"Consul(timeout={self.timeout}, leader_active_id={self.leader_active_id}, engine={self.client})"
