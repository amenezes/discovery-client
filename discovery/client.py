import asyncio
import json
import logging
from functools import partial

import discovery
from discovery.abc import BaseClient
from discovery.exceptions import DiscoveryConnectionError, ServiceNotFoundException
from discovery.filter import Filter
from discovery.utils import select_one_rr

# import aiohttp


logging.getLogger(__name__).addHandler(logging.NullHandler())


class Consul(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.managed_services = {}
        self._leader_id = None

    async def reconnect(self):
        for key, value in self.managed_services.items():
            await self.agent.service.deregister(value.get("id"))
            svc = discovery.service(key, value.get("port"), check=value.get("check"))
            await self.agent.service.register(svc)

        self.__id = await self.leader_current_id()

        logging.debug(f"Consul ID: {self.__id}")
        logging.info("Service successfully re-registered")

    async def leader_ip(self):
        leader_response = await self.status.leader()
        leader_response = await leader_response.json()
        consul_leader, _ = leader_response.split(":")
        return consul_leader

    async def consul_healthy_instances(self):
        health_response = await self.health.service("consul")
        consul_instances = await health_response.json()
        return consul_instances

    async def leader_current_id(self):
        consul_leader = await self.leader_ip()
        consul_instances = await self.consul_healthy_instances()

        current_id = [
            instance.get("Node").get("ID")
            for instance in consul_instances
            if instance.get("Node").get("Address") == consul_leader
        ]

        if current_id is not None:
            current_id = current_id[Filter.FIRST_ITEM.value]

        return current_id

    async def check_consul_health(self):
        while True:
            try:
                await asyncio.sleep(self.timeout)
                current_id = await self.leader_current_id()
                logging.debug(f"Consul ID: {current_id}")

                if current_id != self.__id:
                    await self.reconnect()

            # except aiohttp.ClientConnectorError:
            except DiscoveryConnectionError:
                logging.error("failed to connect to discovery service...")
                logging.error(f"reconnect will occur in {self.timeout} seconds.")
                await asyncio.sleep(self.timeout)
                await self.check_consul_health()

            # except aiohttp.ServerDisconnectedError:
            except DiscoveryConnectionError:
                logging.error(
                    "temporary loss of communication with the discovery server."
                )
                await asyncio.sleep(self.timeout)
                await self.check_consul_health()

    async def find_service(self, name, fn=select_one_rr):
        response = await self.find_services(name)
        if not response:
            raise ServiceNotFoundException
        func = partial(fn, response)
        return func()

    async def find_services(self, name):
        response = await self.catalog.service(name)
        response = await response.json()
        return response

    async def register(self, service_name: str, service_port: int, check=None) -> None:
        svc = discovery.service(service_name, service_port, check=check)
        try:
            await self.agent.service.register(svc)
            self.managed_services[service_name] = {
                "id": f"{json.loads(svc).get('id')}",
                "port": service_port,
                "check": check,
            }
            self.__id = await self.leader_current_id()
            logging.debug(f"Consul ID: {self.__id}")

        #        except aiohttp.ClientConnectorError:
        except DiscoveryConnectionError:
            logging.error("Failed to connect to discovery...")

    async def deregister(self, service_name: str) -> None:
        service = self.managed_services.get(service_name)
        if not service:
            # alterar para servicenotmanaged
            raise ServiceNotFoundException
        await self.agent.service.deregister(service.get("id"))
        self.managed_services.pop(service_name)
