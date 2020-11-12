from discovery.api.abc import Api
from discovery.engine.response import Response


class Raft(Api):
    def __init__(self, endpoint: str = "/operator/raft", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def read_configuration(self, **kwargs) -> Response:
        response: Response = await self.client.get(
            f"{self.url}/configuration", **kwargs
        )
        return response

    async def delete_peer(self, **kwargs) -> Response:
        response: Response = await self.client.delete(f"{self.url}/peer", **kwargs)
        return response
