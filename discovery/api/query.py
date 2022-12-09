from typing import Dict, List, Optional

from discovery.api.abc import Api


class Query(Api):
    def __init__(self, endpoint: str = "/query", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(
        self,
        name: str,
        service: dict,
        session: Optional[str] = None,
        token: Optional[str] = None,
        tags: Optional[List[str]] = None,
        node_meta: Optional[Dict[str, str]] = None,
        service_meta: Optional[Dict[str, str]] = None,
        connect: bool = False,
        dns: Optional[dict] = None,
        dc: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}", dc=dc)
        payload = dict(Name=name, Service=service, Connect=connect)

        if session:
            payload.update({"Session": session})

        if token:
            payload.update({"Token": token})

        if tags:
            payload.update({"Tags": tags})

        if node_meta:
            payload.update({"NodeMeta": node_meta})

        if service_meta:
            payload.update({"ServiceMeta": service_meta})

        if dns:
            payload.update({"DNS": dns})

        async with self.client.post(url, json=payload, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def read(self, uuid: str, dc: Optional[str] = None, **kwargs) -> List[dict]:
        url = self._prepare_request_url(f"{self.url}/{uuid}", dc=dc)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def delete(self, uuid: str, dc: Optional[str] = None, **kwargs) -> None:
        url = self._prepare_request_url(f"{self.url}/{uuid}", dc=dc)
        async with self.client.delete(url, **kwargs):
            pass

    async def update(
        self,
        uuid: str,
        name: str,
        service: dict,
        session: Optional[str] = None,
        token: Optional[str] = None,
        tags: Optional[List[str]] = None,
        node_meta: Optional[Dict[str, str]] = None,
        service_meta: Optional[Dict[str, str]] = None,
        connect: bool = False,
        dns: Optional[dict] = None,
        dc: Optional[str] = None,
        **kwargs,
    ) -> None:
        url = self._prepare_request_url(f"{self.url}/{uuid}", dc=dc)
        payload = dict(Name=name, Service=service, Connect=connect)

        if session:
            payload.update({"Session": session})

        if token:
            payload.update({"Token": token})

        if tags:
            payload.update({"Tags": tags})

        if node_meta:
            payload.update({"NodeMeta": node_meta})

        if service_meta:
            payload.update({"ServiceMeta": service_meta})

        if dns:
            payload.update({"DNS": dns})

        async with self.client.put(url, json=payload, **kwargs):
            pass

    async def execute(
        self,
        uuid: str,
        dc: Optional[str] = None,
        near: Optional[str] = None,
        limit: Optional[int] = None,
        connect: Optional[bool] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(
            f"{self.url}/{uuid}/execute", dc=dc, near=near, limit=limit, connect=connect
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def list(self, dc: Optional[str] = None, **kwargs) -> List[dict]:
        url = self._prepare_request_url(self.url, dc=dc)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def explain(self, uuid: str, dc: Optional[str] = None, **kwargs) -> dict:
        url = self._prepare_request_url(f"{self.url}/{uuid}/explain", dc=dc)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore
