from typing import Optional

from discovery.api.abc import Api
from discovery.api.check_status import CheckStatus


class Checks(Api):
    def __init__(self, endpoint: str = "/agent/check", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def list(
        self, filter: Optional[str] = None, ns: Optional[str] = None, **kwargs
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}s", filter=filter, ns=ns)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def register(self, data: dict, ns: Optional[str] = None, **kwargs) -> None:
        url = self._prepare_request_url(f"{self.url}/register", ns=ns)
        async with self.client.put(url, json=data, **kwargs):
            pass

    async def deregister(
        self, check_id: str, ns: Optional[str] = None, **kwargs
    ) -> None:
        url = self._prepare_request_url(f"{self.url}/deregister/{check_id}", ns=ns)
        async with self.client.put(url, **kwargs):
            pass

    async def check_pass(
        self,
        check_id: str,
        note: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> None:
        url = self._prepare_request_url(f"{self.url}/pass/{check_id}", note=note, ns=ns)
        async with self.client.put(url, **kwargs):
            pass

    async def check_warn(
        self,
        check_id: str,
        note: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> None:
        url = self._prepare_request_url(f"{self.url}/warn/{check_id}", note=note, ns=ns)
        async with self.client.put(url, **kwargs):
            pass

    async def check_fail(
        self,
        check_id: str,
        note: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> None:
        url = self._prepare_request_url(f"{self.url}/fail/{check_id}", note=note, ns=ns)
        async with self.client.put(url, **kwargs):
            pass

    async def check_update(
        self,
        check_id: str,
        status: CheckStatus = CheckStatus.PASSING,
        output: str = "",
        ns: Optional[str] = None,
        **kwargs,
    ) -> None:
        if len([st for st in CheckStatus if status == st]) != 1:
            raise ValueError(
                f"status must be: ['passing', 'warning' or 'critical'] got '{status}'"
            )
        url = self._prepare_request_url(f"{self.url}/update/{check_id}", ns=ns)
        async with self.client.put(
            url, json=dict(status=status, output=output), **kwargs
        ):
            pass
