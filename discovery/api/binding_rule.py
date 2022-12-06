from typing import Optional

from discovery.api.abc import Api


class BindingRule(Api):
    def __init__(self, endpoint: str = "/acl/binding-rule", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(
        self,
        auth_method: str,
        bind_type: str,
        bind_name: str,
        description: str = "",
        selector: str = "",
        namespace: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}", ns=ns)
        payload = dict(
            Description=description,
            AuthMethod=auth_method,
            Selector=selector,
            BindType=bind_type,
            BindName=bind_name,
        )

        if namespace:
            payload.update({"Namespace": namespace})

        async with self.client.put(url, json=payload, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def read(self, role_id: str, ns: Optional[str] = None, **kwargs) -> dict:
        url = self._prepare_request_url(f"{self.url}/{role_id}", ns=ns)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def update(
        self,
        role_id: str,
        auth_method: str,
        bind_type: str,
        bind_name: str,
        description: str = "",
        selector: str = "",
        namespace: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        payload = dict(
            Description=description,
            Selector=selector,
            BindType=bind_type,
            BindName=bind_name,
            AuthMethod=auth_method,
        )

        if namespace:
            payload.update({"Namespace": namespace})

        url = self._prepare_request_url(f"{self.url}/{role_id}", ns=ns)
        async with self.client.put(url, json=payload, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def delete(self, role_id: str, ns: Optional[str] = None, **kwargs) -> bool:
        url = self._prepare_request_url(f"{self.url}/{role_id}", ns=ns)
        async with self.client.delete(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def list(
        self, auth_method: Optional[str] = None, ns: Optional[str] = None, **kwargs
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}", ns=ns)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore
