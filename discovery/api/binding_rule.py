import json

from discovery.api.abc import Api
from discovery.engine.response import Response


class BindingRule(Api):
    def __init__(self, endpoint: str = "/acl/binding-rule", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(self, data, dumps=json.dumps, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}", data=dumps(data), **kwargs
        )
        return response

    async def read(self, role_id, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/{role_id}", **kwargs)
        return response

    async def update(self, data, role_id, dumps=json.dumps, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}/{role_id}", data=dumps(data), **kwargs
        )
        return response

    async def delete(self, role_id, **kwargs) -> Response:
        response: Response = await self.client.delete(f"{self.url}/{role_id}", **kwargs)
        return response

    async def list(self, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}", **kwargs)
        return response
