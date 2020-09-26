from discovery.api.abc import Api


class License(Api):
    def __init__(self, endpoint: str = "/operator/license", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def current(self, **kwargs):
        resp = await self.client.get(f"{self.url}", **kwargs)
        return resp

    async def update(self, data, **kwargs):
        resp = await self.client.put(f"{self.url}", data=data, **kwargs)
        return resp

    async def reset(self, **kwargs):
        response = await self.client.delete(f"{self.url}", **kwargs)
        return response
