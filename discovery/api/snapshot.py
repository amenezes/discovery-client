import json

from discovery.api.abc import Api
from discovery.engine.response import Response


class Snapshot(Api):
    def __init__(self, endpoint: str = "/snapshot", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def generate(self, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}", **kwargs)
        return response

    async def restore(self, data, dumps=json.dumps, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}", data=dumps(data), **kwargs
        )
        return response
