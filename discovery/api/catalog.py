from discovery.api.abc import Api


class Catalog(Api):
    def __init__(self, endpoint: str = "/catalog", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def register(self, data: dict, **kwargs):
        response = await self.client.put(f"{self.url}/register", data=data, **kwargs)
        return response

    async def deregister(self, data, **kwargs):
        response = await self.client.put(f"{self.url}/deregister", **kwargs, data=data)
        return response

    async def datacenters(self, **kwargs):
        response = await self.client.get(f"{self.url}/datacenters", **kwargs)
        return response

    async def nodes(self, **kwargs):
        response = await self.client.get(f"{self.url}/nodes", **kwargs)
        return response

    async def services(self, **kwargs):
        response = await self.client.get(f"{self.url}/services", **kwargs)
        return response

    async def service(self, name, **kwargs):
        response = await self.client.get(f"{self.url}/service/{name}", **kwargs)
        return response

    async def connect(self, service, **kwargs):
        response = await self.client.get(f"{self.url}/connect/{service}", **kwargs)
        return response

    async def node(self, node, **kwargs):
        response = await self.client.get(f"{self.url}/node/{node}", **kwargs)
        return response
