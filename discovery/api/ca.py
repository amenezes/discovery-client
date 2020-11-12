from discovery.api.abc import Api
from discovery.engine.response import Response


class CA(Api):
    def __init__(self, endpoint: str = "/connect/ca", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def roots(self, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/roots", **kwargs)
        return response

    async def configuration(self, **kwargs) -> Response:
        response: Response = await self.client.get(
            f"{self.url}/configuration", **kwargs
        )
        return response

    async def update(self, data, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}/configuration", data=data, **kwargs
        )
        return response
