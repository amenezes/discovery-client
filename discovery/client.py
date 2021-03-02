import asyncio
import os
import pickle

from discovery import api, log, utils
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
        self.timeout = float(os.getenv("DEFAULT_TIMEOUT", 30))
        self._leader_id = None

    async def leader_ip(self) -> str:
        response = await self.status.leader()
        try:
            current_leader = await response.json()
            leader_ip, _ = current_leader.split(":")
        except Exception:
            raise NoConsulLeaderException("Error to identify Consul's leader.")
        return str(leader_ip)

    async def leader_id(self) -> str:
        consul_leader_ip = await self.leader_ip()
        consul_health_instances = await self.health.service("consul")
        consul_health_instances = await consul_health_instances.json()
        current_id = [
            instance["Node"]["ID"]
            for instance in consul_health_instances
            if instance["Node"]["Address"] == consul_leader_ip
        ]
        try:
            return str(current_id[0])
        except Exception:
            raise NoConsulLeaderException

    async def find_services(self, name: str) -> dict:
        response = await self.catalog.service(name)
        resp: dict = await response.json()
        return resp

    async def find_service(self, name: str, fn=utils.select_one_rr) -> list:
        response = await self.find_services(name)
        return fn(response)  # type: ignore

    async def register(self, service, dump_service=True) -> None:
        try:
            await self.agent.service.register(service)
            self._leader_id = await self.leader_id()
            if dump_service:
                with open(".service", "wb") as f:
                    f.write(pickle.dumps(service))
        except Exception as err:
            raise err

    async def deregister(self, service) -> None:
        await self.agent.service.deregister(service["id"])

    async def reconnect(self, service) -> None:
        await self.deregister(service)
        await self.register(service)

    async def watch_connection(self, service) -> None:
        while True:
            try:
                await asyncio.sleep(self.timeout)
                current_id = await self.leader_id()
                if current_id != self._leader_id:
                    await self.reconnect(service)
            except Exception:
                log.error(
                    f"Failed to connect to Consul. Trying a new connection in {self.timeout} seconds."
                )
                await self.watch_connection(service)

    def __repr__(self) -> str:
        return f"Consul(timeout={self.timeout}, leader_id={self._leader_id}, engine={self.client})"
