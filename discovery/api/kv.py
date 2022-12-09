import base64
from typing import Any, List, Optional

from aiohttp import ContentTypeError

from discovery.api.abc import Api


class Kv(Api):
    def __init__(self, endpoint: str = "/kv", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(
        self,
        key: str,
        data: Any,
        dc: Optional[str] = None,
        flags: Optional[int] = None,
        cas: Optional[int] = None,
        acquire: Optional[str] = None,
        release: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> bool:
        url = self._prepare_request_url(
            f"{self.url}/{key}",
            dc=dc,
            flags=flags,
            cas=cas,
            acquire=acquire,
            release=release,
            ns=ns,
        )
        async with self.client.put(url, data=data, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def update(
        self,
        key: str,
        data: Any,
        dc: Optional[str] = None,
        flags: Optional[int] = None,
        cas: Optional[int] = None,
        acquire: Optional[str] = None,
        release: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> bool:
        return await self.create(
            key, data, dc, flags, cas, acquire, release, ns, **kwargs
        )

    async def read(
        self,
        key: str,
        dc: Optional[str] = None,
        recurse: Optional[bool] = None,
        raw: Optional[bool] = None,
        keys: Optional[bool] = None,
        separator: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> List[dict]:
        url = self._prepare_request_url(
            f"{self.url}/{key}",
            dc=dc,
            recurse=recurse,
            raw=raw,
            keys=keys,
            separator=separator,
            ns=ns,
        )
        async with self.client.get(url, **kwargs) as resp:
            try:
                return await resp.json()  # type: ignore
            except ContentTypeError:
                return []

    async def read_value(
        self,
        key: str,
        dc: Optional[str] = None,
        recurse: Optional[bool] = None,
        separator: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> List[bytes]:
        resp = await self.read(
            key, dc=dc, recurse=recurse, separator=separator, ns=ns, **kwargs
        )
        return [base64.b64decode(data["Value"]) for data in resp]

    async def delete(
        self,
        key: str,
        dc: Optional[bool] = None,
        recurse: Optional[str] = None,
        cas: Optional[int] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> bool:
        url = self._prepare_request_url(
            f"{self.url}/{key}", dc=dc, recurse=recurse, cas=cas, ns=ns
        )
        async with self.client.delete(url, **kwargs) as resp:
            return await resp.json()  # type: ignore
