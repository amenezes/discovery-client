from discovery.api.abc import Api
from discovery.engine.response import Response


class Status(Api):
    def __init__(self, endpoint: str = "/status", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def leader(self, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/leader", **kwargs)
        return response

    async def peers(self, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/peers", **kwargs)
        return response
