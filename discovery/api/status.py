from typing import List, Optional

from discovery.api.abc import Api


class Status(Api):
    def __init__(self, endpoint: str = "/status", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def leader(self, dc: Optional[str] = None, **kwargs) -> str:
        url = self._prepare_request_url(f"{self.url}/leader", dc=dc)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def peers(self, dc: Optional[str] = None, **kwargs) -> List[str]:
        url = self._prepare_request_url(f"{self.url}/peers", dc=dc)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore
