import asyncio
import os
from typing import Callable, List, Optional, Union

from discovery import api, log, utils

from .engine.aiohttp import AIOHTTPEngine
from .engine.httpx import HTTPXEngine
from .exceptions import NoConsulLeaderException
from .utils import Service


class Consul:
    def __init__(
        self,
        client: Optional[Union[AIOHTTPEngine, HTTPXEngine]] = None,
        *args,
        **kwargs,
    ):
        self.client = client or AIOHTTPEngine(*args, **kwargs)

        self.catalog = api.Catalog(client=self.client)
        self.config = api.Config(client=self.client)
        self.coordinate = api.Coordinate(client=self.client)
        self.events = api.Events(client=self.client)
        self.health = api.Health(client=self.client)
        self.kv = api.Kv(client=self.client)
        self.namespace = api.Namespace(client=self.client)
        self.query = api.Query(client=self.client)
        self.session = api.Session(client=self.client)
        self.snapshot = api.Snapshot(client=self.client)
        self.status = api.Status(client=self.client)
        self.txn = api.Txn(client=self.client)
        self.agent = api.Agent(client=self.client)
        self.connect = api.Connect(client=self.client)
        self.acl = api.Acl(client=self.client)
        self.operator = api.Operator(client=self.client)
        self.binding_rule = api.BindingRule(client=self.client)
        self.policy = api.Policy(client=self.client)
        self.role = api.Role(client=self.client)
        self.token = api.Token(client=self.client)
        self.check = api.Checks(client=self.client)
        self.services = api.Service(client=self.client)
        self.ca = api.CA(client=self.client)
        self.intentions = api.Intentions(client=self.client)
        self.event = api.Events(client=self.client)

        self.reconnect_timeout = float(
            os.getenv("DISCOVERY_CLIENT_DEFAULT_TIMEOUT", 30)
        )
        self._leader_id: Optional[str] = None

    async def leader_ip(self, *args, **kwargs) -> str:
        try:
            current_leader = await self.status.leader(*args, **kwargs)
            leader_ip, _ = current_leader.split(":")
        except Exception:
            raise NoConsulLeaderException
        return leader_ip

    async def leader_id(self, **kwargs) -> str:
        leader_ip = await self.leader_ip(**kwargs.get("leader_options", {}))
        instances = await self.health.service_instances(
            "consul", **kwargs.get("instance_options", {})
        )
        current_id = [
            instance["Node"]["ID"]
            for instance in instances
            if instance["Node"]["Address"] == leader_ip
        ][0]
        try:
            return str(current_id)
        except Exception:
            raise NoConsulLeaderException

    async def find_services(self, name: str) -> List[dict]:
        return await self.catalog.list_nodes_for_service(name)  # type: ignore

    async def find_service(
        self, name: str, fn: Callable = utils.select_one_rr, *args, **kwargs
    ) -> Optional[dict]:
        response = await self.find_services(name, *args, **kwargs)
        return fn(response)  # type: ignore

    async def register(
        self,
        service: Service,
        enable_watch: bool = False,
        **kwargs,
    ) -> None:
        self._leader_id = await self.leader_id(**kwargs)
        try:
            await self.agent.service.register(service.dict(), **kwargs)
        except Exception as err:
            raise err

        if enable_watch:
            loop = asyncio.get_running_loop()
            loop.create_task(
                self._watch_connection(service, enable_watch, **kwargs),
                name="discovery-client-watch-connection",
            )

    async def deregister(self, service_id: str, ns: Optional[str] = None) -> None:
        await self.agent.service.deregister(service_id, ns)

    async def reconnect(self, service: Service, *args, **kwargs) -> None:
        await self.deregister(service.id)  # type: ignore
        await self.register(service, *args, **kwargs)

    async def _watch_connection(self, service: Service, *args, **kwargs) -> None:
        while True:
            try:
                await asyncio.sleep(self.reconnect_timeout)
                current_id = await self.leader_id()
                if current_id != self._leader_id:
                    await self.reconnect(service, *args, **kwargs)
            except Exception:
                log.error(
                    f"Failed to connect to Consul, trying again at {self.reconnect_timeout}/s"
                )

    def __repr__(self) -> str:
        return f"Consul(engine={self.client})"
