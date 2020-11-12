from discovery.api.abc import Api
from discovery.engine.response import Response


class Health(Api):
    def __init__(self, endpoint: str = "/health", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def node(self, node, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/node/{node}", **kwargs)
        return response

    async def checks(self, service, **kwargs) -> Response:
        response: Response = await self.client.get(
            f"{self.url}/checks/{service}", **kwargs
        )
        return response

    async def service(self, service, **kwargs) -> Response:
        response: Response = await self.client.get(
            f"{self.url}/service/{service}", **kwargs
        )
        return response

    async def connect(self, service, **kwargs) -> Response:
        response: Response = await self.client.get(
            f"{self.url}/connect/{service}", **kwargs
        )
        return response

    async def state(self, state, **kwargs) -> Response:
        state = str(state).lower()
        if state not in ["passing", "warning", "critical"]:
            raise ValueError('Valid values are "passing", "warning", and "critical"')
        response: Response = await self.client.get(
            f"{self.url}/state/{str(state)}", **kwargs
        )
        return response
