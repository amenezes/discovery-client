from typing import List, Optional

from discovery.api.abc import Api
from discovery.api.acl_link import ACLLink


class Namespace(Api):
    def __init__(self, endpoint: str = "/namespace", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(
        self,
        name: str,
        description: str = "",
        acls: Optional[List[ACLLink]] = None,
        meta: Optional[dict] = None,
        **kwargs,
    ) -> dict:
        payload = dict(Name=name, Description=description)
        if acls:
            payload.update({"ACLs": acls})  # type: ignore

        if meta:
            payload.update({"Meta": meta})  # type: ignore

        async with self.client.put(f"{self.url}", json=payload, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def read(self, name: str, **kwargs) -> dict:
        async with self.client.get(f"{self.url}/{name}", **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def update(
        self,
        name: str,
        description: str = "",
        acls: Optional[List[ACLLink]] = None,
        meta: Optional[dict] = None,
        **kwargs,
    ) -> dict:
        payload = dict(Description=description)
        if acls:
            payload.update({"ACLs": acls})  # type: ignore

        if meta:
            payload.update({"Meta": meta})  # type: ignore

        async with self.client.put(
            f"{self.url}/{name}", json=payload, **kwargs
        ) as resp:
            return await resp.json()  # type: ignore

    async def delete(self, name: str, **kwargs) -> dict:
        async with self.client.delete(f"{self.url}/{name}", **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def list_all(self, **kwargs) -> dict:
        async with self.client.get(f"{self.url}s", **kwargs) as resp:
            return await resp.json()  # type: ignore
