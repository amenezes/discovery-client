import json

from discovery.api.abc import Api
from discovery.engine.response import Response


class Query(Api):
    def __init__(self, endpoint: str = "/query", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(self, data, dumps=json.dumps, **kwargs) -> Response:
        response: Response = await self.client.post(
            f"{self.url}", data=dumps(data), **kwargs
        )
        return response

    async def read(self, uuid=None, **kwargs) -> Response:
        if uuid:
            uri = f"{self.url}/{uuid}"
        else:
            uri = f"{self.url}"
        response: Response = await self.client.get(uri, **kwargs)
        return response

    async def delete(self, uuid, **kwargs) -> Response:
        response: Response = await self.client.delete(f"{self.url}/{uuid}", **kwargs)
        return response

    async def update(self, uuid, data, **kwargs) -> Response:
        response: Response = await self.client.put(f"{self.url}/{uuid}", **kwargs)
        return response

    async def execute(self, uuid, **kwargs) -> Response:
        response: Response = await self.client.get(
            f"{self.url}/{uuid}/execute", **kwargs
        )
        return response

    async def explain(self, uuid, **kwargs) -> Response:
        response: Response = await self.client.get(
            f"{self.url}/{uuid}/explain", **kwargs
        )
        return response
