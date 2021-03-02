import base64
import json

from discovery.api.abc import Api
from discovery.engine.response import Response
from discovery.exceptions import KeyNotFoundException


class Kv(Api):
    def __init__(self, endpoint: str = "/kv", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(self, key, data, dumps=json.dumps, **kwargs) -> Response:
        """Create/Update key."""
        response: Response = await self.client.put(
            f"{self.url}/{key}", data=dumps(data), **kwargs
        )
        return response

    async def update(self, key, data, **kwargs) -> Response:
        """Create/Update key."""
        response: Response = await self.create(key, data, **kwargs)
        return response

    async def read(self, key, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/{key}", **kwargs)
        return response

    async def read_value(self, key, **kwargs) -> bytes:
        response = await self.read(key, **kwargs)
        try:
            resp = await response.json()
            return base64.b64decode(resp[0]["Value"])
        except Exception:
            raise KeyNotFoundException(f"Key '{key}' not found.")

    async def delete(self, key, **kwargs) -> Response:
        response: Response = await self.client.delete(f"{self.url}/{key}", **kwargs)
        return response
