from contextlib import asynccontextmanager
from typing import AsyncIterator
from urllib.parse import quote_plus

from discovery import api
from discovery.api.abc import Api
from discovery.engine.response import Response


class Agent(Api):
    def __init__(
        self,
        checks=None,
        connect=None,
        service=None,
        endpoint: str = "/agent",
        **kwargs,
    ) -> None:
        super().__init__(endpoint=endpoint, **kwargs)
        self.checks = checks or api.Checks(client=self.client)
        self.connect = connect or api.Connect(
            api.CA(client=self.client),
            api.Intentions(client=self.client),
            client=self.client,
        )
        self.service = service or api.Service(client=self.client)

    async def members(self, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/members", **kwargs)
        return response

    async def read_configuration(self, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/self", **kwargs)
        return response

    async def reload(self, **kwargs) -> Response:
        response: Response = await self.client.put(f"{self.url}/reload", **kwargs)
        return response

    async def maintenance(self, enable=True, reason=None, **kwargs) -> Response:
        reason = reason or ""
        response: Response = await self.client.put(
            f"{self.url}/maintenance?enable={enable}&reason={quote_plus(reason)}",
            **kwargs,
        )
        return response

    async def metrics(self, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/metrics", **kwargs)
        return response

    @asynccontextmanager
    async def stream_logs(self, chunk_size: int = 20, **kwargs) -> AsyncIterator:
        resp = await self.client.get(f"{self.url}/monitor", **kwargs)
        try:
            yield await resp.content(chunk_size)
        finally:
            await resp.raw_response.close()

    async def join(self, address, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}/join/{address}", **kwargs
        )
        return response

    async def leave(self, **kwargs) -> Response:
        response: Response = await self.client.put(f"{self.url}/leave", **kwargs)
        return response

    async def force_leave(self, node, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}/force-leave/{node}", **kwargs
        )
        return response

    async def update_acl_token(self, token_type: str) -> Response:
        if token_type not in [
            "default",
            "agent",
            "agent_master",
            "replication",
            "acl_token",  # legacy
            "acl_agent_token",
            "acl_agent_master_token",
            "acl_replication_token",
        ]:
            raise ValueError(
                "token_type invalid. See the valid values in: "
                "https://www.consul.io/api/agent.html#update-acl-tokens"
            )
        response: Response = await self.client.put(f"{self.url}/token/{token_type}")
        return response
