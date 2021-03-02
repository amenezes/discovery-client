import json

from discovery.api.abc import Api
from discovery.engine.response import Response


class Events(Api):
    def __init__(self, endpoint: str = "/event", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def fire(self, name, data, dumps=json.dumps, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}/fire/{name}", data=dumps(data), **kwargs
        )
        return response

    async def list(self, key, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/list", **kwargs)
        return response
