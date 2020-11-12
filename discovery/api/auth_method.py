from discovery.api.abc import Api
from discovery.engine.response import Response


class AuthMethod(Api):
    def __init__(self, endpoint: str = "/acl/auth-method", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(self, data, **kwargs) -> Response:
        response: Response = await self.client.put(f"{self.url}", data=data, **kwargs)
        return response

    async def read(self, name, **kwargs) -> Response:
        response: Response = await self.client.put(f"{self.url}/{name}", **kwargs)
        return response

    async def update(self, name, data, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}/{name}", data=data, **kwargs
        )
        return response

    async def delete(self, name, **kwargs) -> Response:
        response: Response = await self.client.delete(f"{self.url}/{name}", **kwargs)
        return response

    async def list(self, **kwargs) -> Response:
        response: Response = await self.client.put(f"{self.url}s", **kwargs)
        return response
