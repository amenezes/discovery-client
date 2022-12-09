from typing import Optional

from discovery.api.abc import Api


class Snapshot(Api):
    def __init__(self, endpoint: str = "/snapshot", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def generate(
        self, dc: Optional[str] = None, stale: Optional[bool] = None, **kwargs
    ) -> bytes:
        url = self._prepare_request_url(f"{self.url}", dc=dc, stale=stale)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.content()  # type: ignore

    async def restore(self, data: bytes, dc: Optional[str] = None, **kwargs) -> None:
        url = self._prepare_request_url(f"{self.url}", dc=dc)
        async with self.client.put(url, data=data, **kwargs):
            pass
