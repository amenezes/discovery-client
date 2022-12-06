from typing import Optional

from discovery.api.abc import Api
from discovery.api.kind import Kind


class Config(Api):
    def __init__(self, endpoint: str = "/config", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def apply(
        self,
        data: dict,
        dc: Optional[str] = None,
        cas: Optional[int] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> None:
        url = self._prepare_request_url(f"{self.url}", dc=dc, cas=cas, ns=ns)
        async with self.client.put(url, json=data, **kwargs):
            pass

    async def get(
        self,
        kind: Kind,
        name: str,
        dc: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}/{kind}/{name}", dc=dc, ns=ns)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def list(
        self, kind: Kind, dc: Optional[str] = None, ns: Optional[str] = None, **kwargs
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}/{kind}", dc=dc, ns=ns)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def delete(
        self,
        kind: Kind,
        name: str,
        dc: Optional[str] = None,
        cas: Optional[int] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> None:
        url = self._prepare_request_url(
            f"{self.url}/{kind}/{name}", dc=dc, cas=cas, ns=ns
        )
        async with self.client.delete(url, **kwargs):
            pass
