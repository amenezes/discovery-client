from typing import Dict, List, Optional

from discovery.api.abc import Api
from discovery.api.token_locality import TokenLocality


class AuthMethod(Api):
    def __init__(self, endpoint: str = "/acl/auth-method", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(
        self,
        name: str,
        type: str,
        description: str,
        config: Dict[str, str],
        display_name: Optional[str] = None,
        max_token_ttl: Optional[str] = None,
        token_locality: Optional[TokenLocality] = None,
        namespace: Optional[str] = None,
        namespace_rules="",
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}", ns=ns)
        payload = dict(Name=name, Type=type, Description=description, Config=config)

        if display_name:
            payload.update({"DisplayName": display_name})

        if max_token_ttl:
            payload.update({"MaxTokenTTL": max_token_ttl})

        if token_locality:
            payload.update({"TokenLocality": token_locality})

        if namespace:
            payload.update({"Namespace": namespace})

        if namespace_rules:
            payload.update({"NamespaceRules": namespace_rules})

        async with self.client.put(url, json=payload, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def read(self, name: str, ns: Optional[str] = None, **kwargs) -> dict:
        url = self._prepare_request_url(f"{self.url}/{name}", ns=ns)
        async with self.client.put(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def update(
        self,
        name: str,
        type: str,
        description: str,
        config: Dict[str, str],
        display_name: Optional[str] = None,
        max_token_ttl: Optional[str] = None,
        token_locality: Optional[TokenLocality] = None,
        namespace: Optional[str] = None,
        namespace_rules="",
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}/{name}", ns=ns)
        payload = dict(Name=name, Type=type, Description=description, Config=config)

        if display_name:
            payload.update({"DisplayName": display_name})

        if max_token_ttl:
            payload.update({"MaxTokenTTL": max_token_ttl})

        if token_locality:
            payload.update({"TokenLocality": token_locality})

        if namespace:
            payload.update({"Namespace": namespace})

        if namespace_rules:
            payload.update({"NamespaceRules": namespace_rules})

        async with self.client.put(url, json=payload, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def delete(self, name: str, ns: Optional[str] = None, **kwargs) -> bool:
        url = self._prepare_request_url(f"{self.url}/{name}", ns=ns)
        async with self.client.delete(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def list(self, ns: Optional[str] = None, **kwargs) -> List[dict]:
        url = self._prepare_request_url(f"{self.url}s", ns=ns)
        async with self.client.put(url, **kwargs) as resp:
            return await resp.json()  # type: ignore
