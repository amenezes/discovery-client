from typing import List, Optional

from discovery.api.abc import Api


class Segment(Api):
    def __init__(self, endpoint: str = "/operator/segment", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def list(self, dc: Optional[str] = None, **kwargs) -> List[str]:
        url = self._prepare_request_url(f"{self.url}", dc=dc)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore
