from discovery.api.abc import Api


class Namespace(Api):
    def __init__(self, endpoint: str = "/namespace", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(self, data, **kwargs):
        response = await self.client.put(f"{self.url}", data=data, **kwargs)
        return response

    async def read(self, name, **kwargs):
        response = await self.client.get(f"{self.url}/{name}", **kwargs)
        return response

    async def update(self, name, data, **kwargs):
        response = await self.client.put(f"{self.url}/{name}", data=data, **kwargs)
        return response

    async def delete(self, name, **kwargs):
        response = await self.client.delete(f"{self.url}/{name}", **kwargs)
        return response

    async def list_all(self, **kwargs):
        response = await self.client.get(f"{self.url}s", **kwargs)
        return response
