from discovery.api.abc import Api


class Status(Api):
    def __init__(self, endpoint: str = "/status", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def leader(self, **kwargs):
        response = await self.client.get(f"{self.url}/leader", params=kwargs)
        return response

    async def peers(self, **kwargs):
        response = await self.client.get(f"{self.url}/peers", params=kwargs)
        return response
