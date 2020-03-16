from discovery.api.abc import Api


class Keyring(Api):
    def __init__(self, endpoint: str = "/operator/keyring", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def list(self, **kwargs):
        response = await self.client.get(f"{self.url}", params=kwargs)
        return response

    async def add(self, data, **kwargs):
        response = await self.client.post(f"{self.url}", data=data, params=kwargs)
        return response

    async def change(self, data, **kwargs):
        response = await self.client.put(f"{self.url}", data=data, params=kwargs)
        return response

    async def delete(self, data, **kwargs):
        response = await self.client.delete(f"{self.url}", data=data, params=kwargs)
        return response
