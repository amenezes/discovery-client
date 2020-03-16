from discovery.api.abc import Api


class License(Api):
    def __init__(self, endpoint: str = "/operator/license", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def current(self, **kwargs):
        resp = await self.client.get(f"{self.url}", params=kwargs)
        return resp

    async def update(self, data, **kwargs):
        resp = await self.client.put(f"{self.url}", params=kwargs, data=data)
        return resp

    async def reset(self, **kwargs):
        response = await self.client.delete(f"{self.url}", params=kwargs)
        return response
