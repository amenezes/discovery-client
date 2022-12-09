from contextlib import asynccontextmanager

from aiohttp import ClientSession

from discovery import log
from discovery.engine.abc import Engine
from discovery.engine.aiohttp.response import AIOHTTPResponse
from discovery.engine.response import Response


class AIOHTTPEngine(Engine):
    def __init__(self, *args, **kwargs) -> None:
        """AIOHTTPEngine.

        args: host, port and scheme
        kwargs: session arguments
        """
        super().__init__(*args)
        self._session_kwargs = kwargs

    @asynccontextmanager
    async def get(self, *args, **kwargs):
        log.debug(f"args: {args}")
        log.debug(f"kwargs: {kwargs}")
        async with ClientSession(**self._session_kwargs) as session:
            log.debug(f"session_kwargs: {self._session_kwargs}")
            response = await session.get(*args, **kwargs)
            response.raise_for_status()
            yield Response(AIOHTTPResponse(response))

    @asynccontextmanager
    async def put(self, *args, **kwargs):
        log.debug(f"args: {args}")
        log.debug(f"kwargs: {kwargs}")
        async with ClientSession(**self._session_kwargs) as session:
            log.debug(f"session_kwargs: {self._session_kwargs}")
            response = await session.put(*args, **kwargs)
            response.raise_for_status()
            yield Response(AIOHTTPResponse(response))

    @asynccontextmanager
    async def delete(self, *args, **kwargs):
        log.debug(f"args: {args}")
        log.debug(f"kwargs: {kwargs}")
        async with ClientSession(**self._session_kwargs) as session:
            log.debug(f"session_kwargs: {self._session_kwargs}")
            response = await session.delete(*args, **kwargs)
            response.raise_for_status()
            yield Response(AIOHTTPResponse(response))

    @asynccontextmanager
    async def post(self, *args, **kwargs):
        log.debug(f"args: {args}")
        log.debug(f"kwargs: {kwargs}")
        async with ClientSession(**self._session_kwargs) as session:
            log.debug(f"session_kwargs: {self._session_kwargs}")
            response = await session.post(*args, **kwargs)
            response.raise_for_status()
            yield Response(AIOHTTPResponse(response))
