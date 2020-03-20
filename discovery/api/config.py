from discovery.api.abc import Api


class Config(Api):
    def __init__(self, endpoint: str = "/config", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    def _config_entry_kind_is_valid(self, kind):
        kind = str(kind).lower()
        if kind not in ["service-defaults", "proxy-defaults"]:
            raise ValueError(
                'Valid values are "service-defaults" and "proxy-defaults".'
            )
        return True

    async def apply(self, data, **kwargs):
        response = await self.client.put(f"{self.url}", params=kwargs, data=data)
        return response

    async def get(self, kind, name, **kwargs):
        if self._config_entry_kind_is_valid(kind):
            response = await self.client.get(f"{self.url}/{kind}/{name}", params=kwargs)
            return response

    async def list(self, kind, **kwargs):
        if self._config_entry_kind_is_valid(kind):
            response = await self.client.get(f"{self.url}/{kind}", params=kwargs)
            return response

    async def delete(self, kind, name, **kwargs):
        if self._config_entry_kind_is_valid(kind):
            response = await self.client.delete(
                f"{self.url}/{kind}/{name}", params=kwargs
            )
            return response
