import json
from urllib.parse import quote_plus

from discovery.api.abc import Api
from discovery.engine.response import Response


class Service(Api):
    def __init__(self, endpoint: str = "/agent/service", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def services(self, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}s", **kwargs)
        return response

    async def service(self, service_id, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/{service_id}", **kwargs)
        return response

    async def configuration(self, service_id, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/{service_id}", **kwargs)
        return response

    async def register(self, data, dumps=json.dumps, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}/register", data=dumps(data), **kwargs
        )
        return response

    async def deregister(self, service_id, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}/deregister/{service_id}", **kwargs
        )
        return response

    async def maintenance(self, service_id, enable, reason="", **kwargs) -> Response:
        reason = quote_plus(reason)
        enable = str(enable).lower()
        response: Response = await self.client.put(
            f"{self.url}/maintenance/{service_id}?enable={enable}&reason={reason}",
            **kwargs,
        )
        return response

    async def service_health_by_name(self, name, **kwargs) -> Response:
        response: Response = await self.client.get(
            f"{self.url}/health/service/name/{name}", **kwargs
        )
        return response

    async def service_health_by_id(self, name, **kwargs) -> Response:
        response: Response = await self.client.get(
            f"{self.url}/health/service/id/{name}", **kwargs
        )
        return response
