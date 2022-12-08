from contextlib import asynccontextmanager

try:
    from httpx import AsyncClient
except ModuleNotFoundError:
    AsyncClient = None  # type: ignore

from discovery import log
from discovery.engine.abc import Engine
from discovery.engine.httpx.response import HTTPXResponse
from discovery.engine.response import Response


class HTTPXEngine(Engine):
    def __init__(self, *args, **kwargs) -> None:
        """HTTPXEngine.

        args: host, port scheme
        kwargs: session arguments
        """
        super().__init__(*args)
        self._session_kwargs = kwargs

    @asynccontextmanager
    async def get(self, *args, **kwargs):
        log.debug(f"args: {args}")
        log.debug(f"kwargs: {kwargs}")
        async with AsyncClient(**self._session_kwargs) as session:
            log.debug(f"session_kwargs: {self._session_kwargs}")
            response = await session.get(*args, **kwargs)
            response.raise_for_status()
            yield Response(HTTPXResponse(response))

    @asynccontextmanager
    async def put(self, *args, **kwargs):
        log.debug(f"args: {args}")
        log.debug(f"kwargs: {kwargs}")
        async with AsyncClient(**self._session_kwargs) as session:
            log.debug(f"session_kwargs: {self._session_kwargs}")
            response = await session.put(*args, **kwargs)
            response.raise_for_status()
            yield Response(HTTPXResponse(response))

    @asynccontextmanager
    async def delete(self, *args, **kwargs):
        log.debug(f"args: {args}")
        log.debug(f"kwargs: {kwargs}")
        async with AsyncClient(**self._session_kwargs) as session:
            log.debug(f"session_kwargs: {self._session_kwargs}")
            response = await session.delete(*args, **kwargs)
            response.raise_for_status()
            yield Response(HTTPXResponse(response))

    @asynccontextmanager
    async def post(self, *args, **kwargs):
        log.debug(f"args: {args}")
        log.debug(f"kwargs: {kwargs}")
        async with AsyncClient(**self._session_kwargs) as session:
            log.debug(f"session_kwargs: {self._session_kwargs}")
            response = await session.post(*args, **kwargs)
            response.raise_for_status()
            yield Response(HTTPXResponse(response))
