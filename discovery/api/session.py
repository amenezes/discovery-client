import json

from discovery.api.abc import Api


class Session(Api):
    def __init__(self, endpoint: str = "/session", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(self, data, dumps=json.dumps, **kwargs):
        response = await self.client.put(
            f"{self.url}/create", data=dumps(data), **kwargs
        )
        return response

    async def delete(self, uuid: str, **kwargs):
        response = await self.client.put(f"{self.url}/destroy/{uuid}", **kwargs)
        return response

    async def read(self, uuid, **kwargs):
        response = await self.client.get(f"{self.url}/info/{uuid}", **kwargs)
        return response

    async def list_node_session(self, node, **kwargs):
        response = await self.client.get(f"{self.url}/node/{node}", **kwargs)
        return response

    async def list(self, **kwargs):
        response = await self.client.get(f"{self.url}/list", **kwargs)
        return response

    async def renew(self, uuid: str, **kwargs):
        response = await self.client.put(f"{self.url}/renew/{uuid}", **kwargs)
        return response
