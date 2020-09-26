from discovery.api.abc import Api


class Events(Api):
    def __init__(self, endpoint: str = "/event", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def fire(self, name, data, **kwargs):
        response = await self.client.put(f"{self.url}/fire/{name}", data=data, **kwargs)
        return response

    async def list(self, key, **kwargs):
        response = await self.client.get(f"{self.url}/list", **kwargs)
        return response
