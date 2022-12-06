from typing import List, Optional

from discovery.api.abc import Api
from discovery.api.health_state import HealthState


class Health(Api):
    def __init__(self, endpoint: str = "/health", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def checks_for_node(
        self,
        node: str,
        dc: Optional[str] = None,
        filter: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> List[dict]:
        url = self._prepare_request_url(
            f"{self.url}/node/{node}", dc=dc, filter=filter, ns=ns
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def checks_for_service(
        self,
        service: str,
        dc: Optional[str] = None,
        near: Optional[str] = None,
        node_meta: Optional[str] = None,
        filter: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> List[dict]:
        url = self._prepare_request_url(
            f"{self.url}/checks/{service}",
            dc=dc,
            near=near,
            node_meta=node_meta,
            filter=filter,
            ns=ns,
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def service_instances(
        self,
        service: str,
        dc: Optional[str] = None,
        near: Optional[str] = None,
        passing: Optional[bool] = None,
        filter: Optional[str] = None,
        peer: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> List[dict]:
        url = self._prepare_request_url(
            f"{self.url}/service/{service}",
            dc=dc,
            near=near,
            passing=passing,
            filter=filter,
            peer=peer,
            ns=ns,
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def service_instances_for_connect(
        self,
        service: str,
        dc: Optional[str] = None,
        near: Optional[str] = None,
        passing: Optional[bool] = None,
        filter: Optional[str] = None,
        peer: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> List[dict]:
        url = self._prepare_request_url(
            f"{self.url}/connect/{service}",
            dc=dc,
            near=near,
            passing=passing,
            filter=filter,
            peer=peer,
            ns=ns,
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def service_instances_for_ingress(
        self,
        service: str,
        dc: Optional[str] = None,
        near: Optional[str] = None,
        passing: Optional[bool] = None,
        filter: Optional[str] = None,
        peer: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> List[dict]:
        url = self._prepare_request_url(
            f"{self.url}/ingress/{service}",
            dc=dc,
            near=near,
            passing=passing,
            filter=filter,
            peer=peer,
            ns=ns,
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def checks_in_state(
        self,
        state: HealthState = HealthState.ANY,
        dc: Optional[str] = None,
        near: Optional[str] = None,
        node_meta: Optional[str] = None,
        filter: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> List[str]:
        url = self._prepare_request_url(
            f"{self.url}/state/{state}",
            dc=dc,
            near=near,
            node_meta=node_meta,
            filter=filter,
            ns=ns,
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore
