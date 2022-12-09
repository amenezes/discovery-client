from typing import Optional
from urllib.parse import quote_plus

from discovery.api.abc import Api


class Service(Api):
    def __init__(self, endpoint: str = "/agent/service", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def list(
        self, filter: Optional[str] = None, ns: Optional[str] = None, **kwargs
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}s", filter=filter, ns=ns)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def configuration(
        self, service_id: str, ns: Optional[str] = None, **kwargs
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}/{service_id}", ns=ns)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def health_by_name(
        self, service_name: str, ns: Optional[str] = None, **kwargs
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}/name/{service_name}", ns=ns)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def health_by_id(
        self, service_id: str, ns: Optional[str] = None, **kwargs
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}/id/{service_id}", ns=ns)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def register(
        self,
        data,
        replace_existing_checks: Optional[bool] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> None:
        url = self._prepare_request_url(
            f"{self.url}/register",
            replace_existing_checks=replace_existing_checks,
            ns=ns,
        )
        async with self.client.put(url, json=data, **kwargs):
            pass

    async def deregister(
        self, service_id: str, ns: Optional[str] = None, **kwargs
    ) -> None:
        url = self._prepare_request_url(f"{self.url}/deregister/{service_id}", ns=ns)
        async with self.client.put(url, **kwargs):
            pass

    async def enable_maintenance(
        self,
        service_id: str,
        enable: Optional[bool] = None,
        reason: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> None:
        if reason:
            reason = quote_plus(reason)
        url = self._prepare_request_url(
            f"{self.url}/maintenance/{service_id}", enable=enable, reason=reason, ns=ns
        )
        async with self.client.put(url, **kwargs):
            pass
