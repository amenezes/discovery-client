import json

from discovery.api.abc import Api
from discovery.engine.response import Response


class Keyring(Api):
    def __init__(self, endpoint: str = "/operator/keyring", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def list(self, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}", **kwargs)
        return response

    async def add(self, data, dumps=json.dumps, **kwargs) -> Response:
        response: Response = await self.client.post(
            f"{self.url}", data=dumps(data), **kwargs
        )
        return response

    async def change(self, data, dumps=json.dumps, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}", data=dumps(data), **kwargs
        )
        return response

    async def delete(self, data, dumps=json.dumps, **kwargs) -> Response:
        response: Response = await self.client.delete(
            f"{self.url}", data=dumps(data), **kwargs
        )
        return response
