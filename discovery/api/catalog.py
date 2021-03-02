import json

from discovery.api.abc import Api
from discovery.engine.response import Response


class Catalog(Api):
    def __init__(self, endpoint: str = "/catalog", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def register(self, data: dict, dumps=json.dumps, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}/register", data=dumps(data), **kwargs
        )
        return response

    async def deregister(self, data, dumps=json.dumps, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}/deregister", **kwargs, data=dumps(data)
        )
        return response

    async def datacenters(self, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/datacenters", **kwargs)
        return response

    async def nodes(self, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/nodes", **kwargs)
        return response

    async def services(self, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/services", **kwargs)
        return response

    async def service(self, name, **kwargs) -> Response:
        response: Response = await self.client.get(
            f"{self.url}/service/{name}", **kwargs
        )
        return response

    async def connect(self, service, **kwargs) -> Response:
        response: Response = await self.client.get(
            f"{self.url}/connect/{service}", **kwargs
        )
        return response

    async def node(self, node, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/node/{node}", **kwargs)
        return response
