from typing import Dict, Optional

from discovery.api.abc import Api


class Catalog(Api):
    def __init__(self, endpoint: str = "/catalog", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def register_entity(
        self,
        address: str,
        datacenter: str,
        node: str,
        node_id: Optional[str] = None,
        tagged_addresses: Optional[Dict[str, str]] = None,
        node_meta: Optional[dict] = None,
        service: Optional[dict] = None,
        check: Optional[dict] = None,
        skip_node_update: bool = False,
        namespace: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> None:
        url = self._prepare_request_url(f"{self.url}/register", ns=ns)
        payload = dict(Datacenter=datacenter, Node=node, Address=address)

        if tagged_addresses:
            payload.update({"TaggedAddresses": tagged_addresses})  # type: ignore

        if node_meta:
            payload.update({"NodeMeta": node_meta})  # type: ignore

        if service:
            payload.update({"Service": service})  # type: ignore

        if check:
            payload.update({"Check": check})  # type: ignore

        if skip_node_update:
            payload.update({"SkipNodeUpdate": skip_node_update})  # type: ignore

        if namespace:
            payload.update({"Namespace": namespace})

        if node_id:
            payload.update({"ID": node_id})

        async with self.client.put(url, json=payload, **kwargs):
            pass

    async def deregister_entity(
        self,
        node: str,
        datacenter: str,
        check_id: Optional[str] = None,
        service_id: Optional[str] = None,
        namespace: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> None:
        url = self._prepare_request_url(f"{self.url}/deregister", ns=ns)
        payload = dict(Node=node, Datacenter=datacenter)

        if check_id:
            payload.update({"CheckID": check_id})

        if service_id:
            payload.update({"ServiceID": service_id})

        if namespace:
            payload.update({"Namespace": namespace})

        async with self.client.put(url, **kwargs, json=payload):
            pass

    async def list_datacenters(self, **kwargs) -> dict:
        async with self.client.get(f"{self.url}/datacenters", **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def list_nodes(
        self,
        dc: Optional[str] = None,
        near: Optional[str] = None,
        filter_options: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(
            f"{self.url}/nodes", dc=dc, near=near, filter=filter_options
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def list_services(
        self,
        dc: Optional[str] = None,
        node_meta: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(
            f"{self.url}/services", dc=dc, node_meta=node_meta, ns=ns
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def list_nodes_for_service(
        self,
        service_name: str,
        dc: Optional[str] = None,
        near: Optional[str] = None,
        filter_options: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(
            f"{self.url}/service/{service_name}",
            dc=dc,
            near=near,
            filter=filter_options,
            ns=ns,
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def list_nodes_for_connect(
        self,
        service: str,
        dc: Optional[str] = None,
        near: Optional[str] = None,
        filter_options: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(
            f"{self.url}/connect/{service}",
            dc=dc,
            near=near,
            filter=filter_options,
            ns=ns,
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def services_for_node(
        self,
        node_name: str,
        dc: Optional[str] = None,
        filter_options: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(
            f"{self.url}/node/{node_name}", dc=dc, filter=filter_options, ns=ns
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def list_services_for_node(
        self,
        node_name: str,
        dc: Optional[str] = None,
        filter_options: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(
            f"{self.url}/node-services/{node_name}", dc=dc, filter=filter_options, ns=ns
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def list_services_for_gateway(
        self,
        gateway: str,
        dc: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(
            f"{self.url}/gateway-services/{gateway}", dc=dc, ns=ns
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore
