from contextlib import asynccontextmanager

try:
    from httpx import AsyncClient
except ModuleNotFoundError:
    AsyncClient = None  # type: ignore

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
        async with AsyncClient(**self._session_kwargs) as session:
            response = await session.get(*args, **kwargs)
            yield Response(HTTPXResponse(response))

    @asynccontextmanager
    async def put(self, *args, **kwargs):
        async with AsyncClient(**self._session_kwargs) as session:
            response = await session.put(*args, **kwargs)
            yield Response(HTTPXResponse(response))

    @asynccontextmanager
    async def delete(self, *args, **kwargs):
        async with AsyncClient(**self._session_kwargs) as session:
            response = await session.delete(*args, **kwargs)
            yield Response(HTTPXResponse(response))

    @asynccontextmanager
    async def post(self, *args, **kwargs):
        async with AsyncClient(**self._session_kwargs) as session:
            response = await session.post(*args, **kwargs)
            yield Response(HTTPXResponse(response))
