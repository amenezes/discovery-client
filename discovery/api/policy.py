import json

from discovery.api.abc import Api
from discovery.engine.response import Response


class Policy(Api):
    def __init__(self, endpoint: str = "/acl/policy", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(self, data, dumps=json.dumps, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}", data=dumps(data), **kwargs
        )
        return response

    async def read(self, policy_id, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/{policy_id}", **kwargs)
        return response

    async def update(self, policy_id, data, dumps=json.dumps, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}/{policy_id}", data=dumps(data), **kwargs
        )
        return response

    async def delete(self, policy_id, **kwargs) -> Response:
        response: Response = await self.client.delete(
            f"{self.url}/{policy_id}", **kwargs
        )
        return response

    async def list(self, **kwargs) -> Response:
        url = self.url.replace("policy", "policies")
        response: Response = await self.client.get(f"{url}", **kwargs)
        return response
