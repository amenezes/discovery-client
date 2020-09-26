from discovery.api.abc import Api


class AutoPilot(Api):
    def __init__(self, endpoint: str = "/operator/autopilot", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def read_configuration(self, **kwargs):
        response = await self.client.get(f"{self.url}/configuration", **kwargs)
        return response

    async def update_configuration(self, data, **kwargs):
        response = await self.client.put(
            f"{self.url}/configuration", data=data, **kwargs
        )
        return response

    async def read_health(self, **kwargs):
        response = await self.client.get(f"{self.url}/health", **kwargs)
        return response
