from typing import Any, Optional

from discovery.api.abc import Api


class License(Api):
    def __init__(self, endpoint: str = "/operator/license", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def current(self, dc: Optional[str] = None, **kwargs) -> dict:
        url = self._prepare_request_url(f"{self.url}", dc=dc)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def update(self, data: Any, dc: Optional[str] = None, **kwargs) -> dict:
        url = self._prepare_request_url(f"{self.url}", dc=dc)
        async with self.client.put(url, data=data, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def reset(self, dc: Optional[str] = None, **kwargs) -> dict:
        url = self._prepare_request_url(f"{self.url}", dc=dc)
        async with self.client.delete(url, **kwargs) as resp:
            return await resp.json()  # type: ignore
