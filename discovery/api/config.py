import json

from discovery.api.abc import Api
from discovery.engine.response import Response


class Config(Api):
    def __init__(self, endpoint: str = "/config", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    def _config_entry_kind_is_valid(self, kind) -> bool:
        kind = str(kind).lower()
        if kind not in ["service-defaults", "proxy-defaults"]:
            raise ValueError(
                'Valid values are "service-defaults" and "proxy-defaults".'
            )
        return True

    async def apply(self, data, dumps=json.dumps, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}", data=dumps(data), **kwargs
        )
        return response

    async def get(self, kind, name, **kwargs) -> Response:
        self._config_entry_kind_is_valid(kind)
        response: Response = await self.client.get(
            f"{self.url}/{kind}/{name}", **kwargs
        )
        return response

    async def list(self, kind, **kwargs) -> Response:
        self._config_entry_kind_is_valid(kind)
        response: Response = await self.client.get(f"{self.url}/{kind}", **kwargs)
        return response

    async def delete(self, kind, name, **kwargs) -> Response:
        self._config_entry_kind_is_valid(kind)
        response: Response = await self.client.delete(
            f"{self.url}/{kind}/{name}", **kwargs
        )
        return response
