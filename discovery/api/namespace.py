import json

from discovery.api.abc import Api
from discovery.engine.response import Response


class Namespace(Api):
    def __init__(self, endpoint: str = "/namespace", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(self, data, dumps=json.dumps, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}", data=dumps(data), **kwargs
        )
        return response

    async def read(self, name, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/{name}", **kwargs)
        return response

    async def update(self, name, data, dumps=json.dumps, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}/{name}", data=dumps(data), **kwargs
        )
        return response

    async def delete(self, name, **kwargs) -> Response:
        response: Response = await self.client.delete(f"{self.url}/{name}", **kwargs)
        return response

    async def list_all(self, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}s", **kwargs)
        return response
