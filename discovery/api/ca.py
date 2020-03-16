from discovery.api.abc import Api


class CA(Api):
    def __init__(self, endpoint: str = "/connect/ca", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def roots(self, **kwargs):
        response = await self.client.get(f"{self.url}/roots", params=kwargs)
        return response

    async def configuration(self, **kwargs):
        response = await self.client.get(f"{self.url}/configuration", params=kwargs)
        return response

    async def update(self, data, **kwargs):
        response = await self.client.put(
            f"{self.url}/configuration", data=data, params=kwargs
        )
        return response
