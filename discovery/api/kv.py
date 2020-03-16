from discovery.api.abc import Api


class Kv(Api):
    def __init__(self, endpoint: str = "/kv", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(self, key, data, **kwargs):
        response = await self.update(key, data, **kwargs)
        return response

    async def read(self, key, **kwargs):
        response = await self.client.get(f"{self.url}/{key}", params=kwargs)
        return response

    async def update(self, key, data, **kwargs):
        response = await self.client.put(f"{self.url}/{key}", params=kwargs, data=data)
        return response

    async def delete(self, key, **kwargs):
        response = await self.client.delete(f"{self.url}/{key}", params=kwargs)
        return response
