from discovery.api.abc import Api
from discovery.engine.response import Response


class Segment(Api):
    def __init__(self, endpoint: str = "/operator/segment", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def list(self, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}", **kwargs)
        return response
