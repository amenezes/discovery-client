from discovery.api.abc import Api


class Health(Api):
    def __init__(self, endpoint: str = "/health", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def node(self, node, **kwargs):
        response = await self.client.get(f"{self.url}/node/{node}", **kwargs)
        return response

    async def checks(self, service, **kwargs):
        response = await self.client.get(f"{self.url}/checks/{service}", **kwargs)
        return response

    async def service(self, service, **kwargs):
        response = await self.client.get(f"{self.url}/service/{service}", **kwargs)
        return response

    async def connect(self, service, **kwargs):
        response = await self.client.get(f"{self.url}/connect/{service}", **kwargs)
        return response

    async def state(self, state, **kwargs):
        state = str(state).lower()
        if state not in ["passing", "warning", "critical"]:
            raise ValueError('Valid values are "passing", "warning", and "critical"')
        response = await self.client.get(f"{self.url}/state/{str(state)}", **kwargs)
        return response
