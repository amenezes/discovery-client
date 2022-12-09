from typing import Optional

from discovery.api.abc import Api


class Txn(Api):
    def __init__(self, endpoint: str = "/txn", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(self, data: dict, dc: Optional[str] = None, **kwargs) -> dict:
        url = self._prepare_request_url(f"{self.url}", dc=dc)
        async with self.client.put(url, json=data, **kwargs) as resp:
            return await resp.json()  # type: ignore
