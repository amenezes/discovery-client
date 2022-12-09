from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional
from urllib.parse import quote_plus

from discovery import api, log
from discovery.api.abc import Api
from discovery.api.loglevel import LogLevel
from discovery.api.token_type import TokenType


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

    async def host_information(self, **kwargs) -> dict:
        async with self.client.get(f"{self.url}/host", **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def members(
        self, wan: Optional[bool] = None, segment: Optional[str] = None, **kwargs
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}/members", wan=wan, segment=segment)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def read_configuration(self, **kwargs) -> dict:
        async with self.client.get(f"{self.url}/self", **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def reload(self, **kwargs) -> None:
        async with self.client.put(f"{self.url}/reload", **kwargs):
            pass

    async def maintenance(
        self, enable: bool = True, reason: Optional[str] = None, **kwargs
    ) -> None:
        if reason:
            reason = quote_plus(reason)
        url = self._prepare_request_url(
            f"{self.url}/maintenance", enable=enable, reason=reason
        )
        async with self.client.put(url, **kwargs):
            pass

    async def metrics(self, **kwargs) -> dict:
        async with self.client.get(f"{self.url}/metrics", **kwargs) as resp:
            return await resp.json()  # type: ignore

    @asynccontextmanager
    async def stream_logs(
        self,
        loglevel: LogLevel = LogLevel.INFO,
        logjson: bool = False,
        chunk_size: int = 1000,
        **kwargs,
    ) -> AsyncIterator:
        url = self._prepare_request_url(
            f"{self.url}/monitor", loglevel=loglevel, logjson=logjson
        )
        async with self.client.get(url, **kwargs) as resp:
            yield await resp.content(chunk_size)

    async def join(self, address: str, wan: Optional[bool] = None, **kwargs) -> None:
        url = self._prepare_request_url(f"{self.url}/join/{address}", wan=wan)
        async with self.client.put(url, **kwargs):
            pass

    async def leave(self, **kwargs) -> None:
        async with self.client.put(f"{self.url}/leave", **kwargs):
            pass

    async def force_leave(
        self,
        node_name: str,
        prune: Optional[bool] = None,
        wan: Optional[bool] = None,
        **kwargs,
    ) -> None:
        url = self._prepare_request_url(
            f"{self.url}/force-leave/{node_name}", prune=prune, wan=wan
        )
        async with self.client.put(url, **kwargs):
            pass

    async def update_acl_token(self, token: str, token_type: TokenType) -> dict:
        if token_type == TokenType.AGENT_MASTER:
            log.warning("Deprecated in version 1.11")
        elif token_type in [
            TokenType.ACL_TOKEN,
            TokenType.ACL_AGENT_TOKEN,
            TokenType.ACL_AGENT_MASTER_TOKEN,
            TokenType.ACL_REPLICATION_TOKEN,
        ]:
            log.warning("Deprecated in version 1.4.3")
        async with self.client.put(
            f"{self.url}/token/{token_type}", json={"Token": token}
        ) as resp:
            return await resp.json()  # type: ignore
