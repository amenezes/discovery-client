from typing import List, Optional

from discovery.api.abc import Api
from discovery.api.intention_by import IntentionBy
from discovery.api.intention_filter import IntentionFilter
from discovery.api.intentions_action import IntentionsAction


class Intentions(Api):
    def __init__(self, endpoint: str = "/connect/intentions", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def upsert_by_name(
        self,
        source: str,
        destination: str,
        ns: Optional[str] = None,
        source_type: str = "consul",
        action: IntentionsAction = IntentionsAction.ALLOW,
        permissions: Optional[List[str]] = None,
        description: str = "",
        **kwargs,
    ) -> bool:
        payload = dict(SourceType=source_type, Action=action, Description=description)

        if permissions:
            payload.update({"Permissions": permissions})  # type: ignore

        url = self._prepare_request_url(
            f"{self.url}/exact", source=source, destination=destination, ns=ns
        )
        async with self.client.put(url, json=payload, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def read_by_name(
        self, source: str, destination: str, ns: Optional[str] = None, **kwargs
    ):
        url = self._prepare_request_url(
            f"{self.url}/exact", source=source, destination=destination, ns=ns
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()

    async def list(
        self,
        filter: IntentionFilter = IntentionFilter.SOURCE_NAME,
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}", filter=filter, ns=ns)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def delete_by_name(
        self, source: str, destination: str, ns: Optional[str] = None, **kwargs
    ) -> None:
        url = self._prepare_request_url(
            f"{self.url}/exact", source=source, destination=destination, ns=ns
        )
        async with self.client.delete(url, **kwargs):
            pass

    async def check(
        self, source: str, destination: str, ns: Optional[str] = None, **kwargs
    ) -> dict:
        url = self._prepare_request_url(
            f"{self.url}/check", source=source, destination=destination, ns=ns
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def list_match(
        self,
        name: str,
        by: IntentionBy = IntentionBy.NAME,
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}/match", by=by, name=name, ns=ns)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore
