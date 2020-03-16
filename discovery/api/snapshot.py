from discovery.api.abc import Api


class Snapshot(Api):
    def __init__(self, endpoint: str = "/snapshot", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def generate(self, **kwargs):
        response = await self.client.get(f"{self.url}", params=kwargs)
        return response

    async def restore(self, data, **kwargs):
        response = await self.client.put(f"{self.url}", data=data, params=kwargs)
        return response
