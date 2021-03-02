import json

from discovery.api.abc import Api
from discovery.engine.response import Response


class Txn(Api):
    def __init__(self, endpoint: str = "/txn", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(self, data, dumps=json.dumps, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}", data=dumps(data), **kwargs
        )
        return response
