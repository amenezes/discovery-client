from aiohttp import ClientSession

from discovery.engine.abc import Engine
from discovery.engine.aiohttp_response import AIOHTTPResponse
from discovery.engine.response import Response


class AIOHTTPEngine(Engine):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    async def get(self, *args, **kwargs) -> Response:
        async with ClientSession() as session:
            response = await session.get(*args, **kwargs)
            return Response(AIOHTTPResponse(response))

    async def put(self, *args, **kwargs) -> Response:
        async with ClientSession() as session:
            response = await session.put(*args, **kwargs)
            return Response(AIOHTTPResponse(response))

    async def delete(self, *args, **kwargs) -> Response:
        async with ClientSession() as session:
            response = await session.delete(*args, **kwargs)
            return Response(AIOHTTPResponse(response))

    async def post(self, *args, **kwargs) -> Response:
        async with ClientSession() as session:
            response = await session.post(*args, **kwargs)
            return Response(AIOHTTPResponse(response))
