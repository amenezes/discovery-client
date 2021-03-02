from httpx import AsyncClient

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

    async def get(self, *args, **kwargs) -> Response:
        async with AsyncClient(**self._session_kwargs) as session:
            response = await session.get(*args, **kwargs)
            return Response(HTTPXResponse(response))

    async def put(self, *args, **kwargs) -> Response:
        async with AsyncClient(**self._session_kwargs) as session:
            response = await session.put(*args, **kwargs)
            return Response(HTTPXResponse(response))

    async def delete(self, *args, **kwargs) -> Response:
        async with AsyncClient(**self._session_kwargs) as session:
            response = await session.delete(*args, **kwargs)
            return Response(HTTPXResponse(response))

    async def post(self, *args, **kwargs) -> Response:
        async with AsyncClient(**self._session_kwargs) as session:
            response = await session.post(*args, **kwargs)
            return Response(HTTPXResponse(response))
