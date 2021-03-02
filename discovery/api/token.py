import json

from discovery.api.abc import Api


class Token(Api):
    def __init__(self, endpoint: str = "/acl/token", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(self, data, dumps=json.dumps, **kwargs):
        response = await self.client.put(f"{self.url}", data=dumps(data), **kwargs)
        return response

    async def read_by_id(self, role_id, **kwargs):
        response = await self.client.get(f"{self.url}/{role_id}", **kwargs)
        return response

    async def read_by_name(self, name: str, **kwargs):
        response = await self.client.get(f"{self.url}/name/{name}", **kwargs)
        return response

    async def details(self, headers: dict = {}):
        response = await self.client.get(f"{self.url}/self", headers=headers)
        return response

    async def clone(self, accessor_id: str, **kwargs):
        response = await self.client.put(f"{self.url}/{accessor_id}/clone", **kwargs)
        return response

    async def update(self, role_id, data, dumps=json.dumps, **kwargs):
        response = await self.client.put(
            f"{self.url}/{role_id}", data=dumps(data), **kwargs
        )
        return response

    async def delete(self, role_id, **kwargs):
        response = await self.client.delete(f"{self.url}/{role_id}", **kwargs)
        return response

    async def list(self, **kwargs):
        response = await self.client.get(f"{self.url}s", **kwargs)
        return response
