from discovery.api.abc import Api


class Raft(Api):
    def __init__(self, endpoint: str = "/operator/raft", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def read_configuration(self, **kwargs):
        response = await self.client.get(f"{self.url}/configuration", params=kwargs)
        return response

    async def delete_peer(self, **kwargs):
        response = await self.client.delete(f"{self.url}/peer", params=kwargs)
        return response
