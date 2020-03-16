from discovery.api.abc import Api


class Coordinate(Api):
    def __init__(self, endpoint: str = "/coordinate", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def read_wan(self, **kwargs):
        response = await self.client.get(f"{self.url}/datacenters", params=kwargs)
        return response

    async def read_lan(self, **kwargs):
        response = await self.client.get(f"{self.url}/nodes", params=kwargs)
        return response

    async def read_lan_node(self, node, **kwargs):
        response = await self.client.get(f"{self.url}/node/{node}", params=kwargs)
        return response

    async def update_lan_node(self, data, **kwargs):
        response = await self.client.put(f"{self.url}/update", params=kwargs, data=data)
        return response
