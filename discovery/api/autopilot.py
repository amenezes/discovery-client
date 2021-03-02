import json

from discovery.api.abc import Api
from discovery.engine.response import Response


class AutoPilot(Api):
    def __init__(self, endpoint: str = "/operator/autopilot", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def read_configuration(self, **kwargs) -> Response:
        response: Response = await self.client.get(
            f"{self.url}/configuration", **kwargs
        )
        return response

    async def update_configuration(self, data, dumps=json.dumps, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}/configuration", data=dumps(data), **kwargs
        )
        return response

    async def read_health(self, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/health", **kwargs)
        return response
