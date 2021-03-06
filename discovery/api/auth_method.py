from discovery.api.abc import Api


class AuthMethod(Api):
    def __init__(self, endpoint: str = "/acl/auth-method", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(self, data, **kwargs):
        response = await self.client.put(f"{self.url}", data=data, **kwargs)
        return response

    async def read(self, name, **kwargs):
        response = await self.client.put(f"{self.url}/{name}", **kwargs)
        return response

    async def update(self, name, data, **kwargs):
        response = await self.client.put(f"{self.url}/{name}", data=data, **kwargs)
        return response

    async def delete(self, name, **kwargs):
        response = await self.client.delete(f"{self.url}/{name}", **kwargs)
        return response

    async def list(self, **kwargs):
        response = await self.client.put(f"{self.url}s", **kwargs)
        return response
