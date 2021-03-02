import json

from discovery.api.abc import Api
from discovery.engine.response import Response


class Coordinate(Api):
    def __init__(self, endpoint: str = "/coordinate", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def read_wan(self, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/datacenters", **kwargs)
        return response

    async def read_lan(self, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/nodes", **kwargs)
        return response

    async def read_lan_node(self, node, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/node/{node}", **kwargs)
        return response

    async def update_lan_node(self, data, dumps=json.dumps, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}/update", data=dumps(data), **kwargs
        )
        return response
