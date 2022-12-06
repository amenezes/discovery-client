from typing import List, Optional

from discovery.api.abc import Api


class Role(Api):
    def __init__(self, endpoint: str = "/acl/role", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(
        self,
        name: str,
        description: str,
        policies: List[dict],
        service_identities: Optional[List[dict]] = None,
        node_identities: Optional[List[dict]] = None,
        namespace: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}", ns=ns)
        payload = dict(Name=name, Description=description, Policies=policies)

        if service_identities:
            payload.update({"ServiceIdentities": service_identities})

        if node_identities:
            payload.update({"NodeIdentities": node_identities})

        if namespace:
            payload.update({"Namespace": namespace})

        async with self.client.put(url, json=payload, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def read_by_id(
        self, role_id: str, ns: Optional[str] = None, **kwargs
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}/{role_id}", ns=ns)
        async with self.client.put(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def read_by_name(self, name: str, ns: Optional[str] = None, **kwargs) -> dict:
        url = self._prepare_request_url(f"{self.url}/name/{name}", ns=ns)
        async with self.client.put(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def update(
        self,
        role_id: str,
        name: str,
        description: str,
        policies: List[dict],
        service_identities: Optional[List[dict]] = None,
        node_identities: Optional[List[dict]] = None,
        namespace: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}/{role_id}", ns=ns)
        payload = dict(Name=name, Description=description, Policies=policies)

        if service_identities:
            payload.update({"ServiceIdentities": service_identities})

        if node_identities:
            payload.update({"NodeIdentities": node_identities})

        if namespace:
            payload.update({"Namespace": namespace})
        async with self.client.put(url, json=payload, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def delete(self, role_id: str, ns: Optional[str] = None, **kwargs) -> bool:
        url = self._prepare_request_url(f"{self.url}/{role_id}", ns=ns)
        async with self.client.delete(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def list(
        self, policy: Optional[str] = None, ns: Optional[str] = None, **kwargs
    ) -> List[dict]:
        url = self._prepare_request_url(f"{self.url}s", policy=policy, ns=ns)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore
