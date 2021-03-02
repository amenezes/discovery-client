import json

from discovery.api.abc import Api
from discovery.engine.response import Response


class License(Api):
    def __init__(self, endpoint: str = "/operator/license", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def current(self, **kwargs) -> Response:
        resp: Response = await self.client.get(f"{self.url}", **kwargs)
        return resp

    async def update(self, data, dumps=json.dumps, **kwargs) -> Response:
        resp: Response = await self.client.put(
            f"{self.url}", data=dumps(data), **kwargs
        )
        return resp

    async def reset(self, **kwargs) -> Response:
        response: Response = await self.client.delete(f"{self.url}", **kwargs)
        return response
