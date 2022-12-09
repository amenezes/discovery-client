from typing import Dict, List, Optional

from discovery.api.abc import Api
from discovery.api.behavior import Behavior


class Session(Api):
    def __init__(self, endpoint: str = "/session", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(
        self,
        name: str,
        node: Optional[str] = None,
        lock_delay: str = "15s",
        checks: Optional[List[str]] = None,
        node_checks: Optional[List[str]] = None,
        service_checks: Optional[Dict[str, str]] = None,
        behavior: Behavior = Behavior.RELEASE,
        ttl: Optional[str] = None,
        ns: Optional[str] = None,
        dc: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}/create", ns=ns, dc=dc)
        payload = dict(Name=name, LockDelay=lock_delay)

        if node:
            payload.update({"Node": node})

        if checks:
            payload.update({"Checks": checks})  # type: ignore

        if node_checks:
            payload.update({"NodeChecks": node_checks})  # type: ignore

        if service_checks:
            payload.update({"ServiceChecks": service_checks})  # type: ignore

        if behavior:
            payload.update({"Behavior": behavior})

        if ttl:
            payload.update({"TTL": ttl})

        async with self.client.put(url, json=payload, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def delete(
        self, uuid: str, dc: Optional[str] = None, ns: Optional[str] = None, **kwargs
    ) -> bool:
        url = self._prepare_request_url(f"{self.url}/destroy/{uuid}", dc=dc, ns=ns)
        async with self.client.put(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def read(
        self, uuid: str, dc: Optional[str] = None, ns: Optional[str] = None, **kwargs
    ) -> List[dict]:
        url = self._prepare_request_url(f"{self.url}/info/{uuid}", dc=dc, ns=ns)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def list_sessions_for_node(
        self, node: str, dc: Optional[str] = None, ns: Optional[str] = None, **kwargs
    ) -> List[dict]:
        url = self._prepare_request_url(f"{self.url}/node/{node}", dc=dc, ns=ns)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def list(
        self, dc: Optional[str] = None, ns: Optional[str] = None, **kwargs
    ) -> List[dict]:
        url = self._prepare_request_url(f"{self.url}/list", dc=dc, ns=ns)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def renew(
        self, uuid: str, dc: Optional[str] = None, ns: Optional[str] = None, **kwargs
    ) -> List[dict]:
        url = self._prepare_request_url(f"{self.url}/renew/{uuid}", ns=ns, dc=dc)
        async with self.client.put(url, **kwargs) as resp:
            return await resp.json()  # type: ignore
