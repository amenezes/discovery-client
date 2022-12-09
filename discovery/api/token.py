from typing import Any, List, Optional

from discovery.api.abc import Api


class Token(Api):
    def __init__(self, endpoint: str = "/acl/token", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(
        self,
        description: str,
        policies: Optional[List[dict]] = None,
        roles: Optional[List[dict]] = None,
        service_identities: Optional[List[dict]] = None,
        node_identities: Optional[List[dict]] = None,
        local: bool = False,
        expiration_time: Optional[Any] = None,
        expiration_ttl: Optional[Any] = None,
        namespace: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}", ns=ns)
        payload = dict(Description=description, local=local)

        if policies:
            payload.update({"Policies": policies})

        if roles:
            payload.update({"Roles": roles})

        if service_identities:
            payload.update({"ServiceIdentities": service_identities})

        if node_identities:
            payload.update({"NodeIdentities": node_identities})

        if expiration_time:
            payload.update({"ExpirationTime": expiration_time})

        if expiration_ttl:
            payload.update({"ExpirationTTL": expiration_ttl})

        if namespace:
            payload.update({"Namespace": namespace})

        async with self.client.put(url, json=payload, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def read(
        self,
        accessor_id: str,
        ns: Optional[str] = None,
        expanded: Optional[bool] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(
            f"{self.url}/{accessor_id}", ns=ns, expanded=expanded
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def details(self, headers: dict = {}) -> dict:
        async with self.client.get(f"{self.url}/self", headers=headers) as resp:
            return await resp.json()  # type: ignore

    async def update(
        self,
        accessor_id: str,
        description: str,
        secret_id: Optional[str] = None,
        policies: Optional[List[dict]] = None,
        roles: Optional[List[dict]] = None,
        service_identities: Optional[List[dict]] = None,
        node_identities: Optional[List[dict]] = None,
        local: bool = False,
        auth_method: Optional[str] = None,
        expiration_time: Optional = None,  # type: ignore
        namespace: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}/{accessor_id}", ns=ns)
        payload = dict(SecretID=secret_id, Description=description, Local=local)

        if secret_id:
            payload.update({"SecretID": secret_id})

        if policies:
            payload.update({"Policies": policies})  # type: ignore

        if roles:
            payload.update({"Roles": roles})  # type: ignore

        if service_identities:
            payload.update({"ServiceIdentities": service_identities})  # type: ignore

        if node_identities:
            payload.update({"NodeIdentities": node_identities})  # type: ignore

        if auth_method:
            payload.update({"AuthMethod": auth_method})

        if expiration_time:
            payload.update({"ExpirationTime": expiration_time})

        if namespace:
            payload.update({"Namespace": namespace})

        async with self.client.put(url, json=payload, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def clone(
        self,
        accessor_id: str,
        description: str,
        namespace: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}/{accessor_id}/clone", ns=ns)
        payload = dict(Description=description)

        if namespace:
            payload.update({"Namespace": namespace})

        async with self.client.put(url, json=payload, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def delete(
        self, accessor_id: str, ns: Optional[str] = None, **kwargs
    ) -> bool:
        url = self._prepare_request_url(f"{self.url}/{accessor_id}", ns=ns)
        async with self.client.delete(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def list(
        self,
        policy: Optional[str] = None,
        role: Optional[str] = None,
        auth_method: Optional[str] = None,
        auth_method_ns: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(
            f"{self.url}s",
            policy=policy,
            role=role,
            authmethod=auth_method,
            authmethod_ns=auth_method_ns,
            ns=ns,
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore
