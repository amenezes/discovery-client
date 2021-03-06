from discovery.api.abc import Api
from discovery.engine.response import HttpResponse


class Txn(Api):
    def __init__(self, endpoint: str = "/txn", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(self, data, **kwargs):
        response = await self.client.put(f"{self.url}", data=data, **kwargs)
        return HttpResponse(response)
