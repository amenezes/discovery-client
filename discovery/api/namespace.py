from discovery.api.abc import Api


class Namespace(Api):
    def __init__(self, endpoint: str = "/namespace", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(self, data, **kwargs):
        resp = await self.client.put(f"{self.url}", data=data, params=kwargs)
        return resp

    async def read(self, name, **kwargs):
        resp = await self.client.get(f"{self.url}/{name}", params=kwargs)
        return resp

    async def update(self, name, data, **kwargs):
        response = await self.client.put(f"{self.url}/{name}", data=data, params=kwargs)
        return response

    async def delete(self, name, **kwargs):
        response = await self.client.delete(f"{self.url}/{name}", params=kwargs)
        return response

    async def list_all(self, **kwargs):
        response = await self.client.get(f"{self.url}s", params=kwargs)
        return response
