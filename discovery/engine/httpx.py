from httpx import AsyncClient

from discovery.engine.abc import Engine
from discovery.engine.httpx_response import HTTPXResponse
from discovery.engine.response import Response


class HTTPXEngine(Engine):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    async def get(self, *args, **kwargs) -> Response:
        async with AsyncClient() as session:
            response = await session.get(*args, **kwargs)
            return Response(HTTPXResponse(response))

    async def put(self, *args, **kwargs) -> Response:
        async with AsyncClient() as session:
            response = await session.put(*args, **kwargs)
            return Response(HTTPXResponse(response))

    async def delete(self, *args, **kwargs) -> Response:
        async with AsyncClient() as session:
            response = await session.delete(*args, **kwargs)
            return Response(HTTPXResponse(response))

    async def post(self, *args, **kwargs) -> Response:
        async with AsyncClient() as session:
            response = await session.post(*args, **kwargs)
            return Response(HTTPXResponse(response))
