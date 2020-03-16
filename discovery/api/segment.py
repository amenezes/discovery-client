from discovery.api.abc import Api


class Segment(Api):
    def __init__(self, endpoint: str = "/operator/segment", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def list(self, **kwargs):
        response = await self.client.get(f"{self.url}", params=kwargs)
        return response
