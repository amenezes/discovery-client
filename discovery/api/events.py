from typing import Optional

from discovery.api.abc import Api


class Events(Api):
    def __init__(self, endpoint: str = "/event", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def fire_event(
        self,
        name: str,
        data: dict,
        dc: Optional[str] = None,
        node: Optional[str] = None,
        service: Optional[str] = None,
        tag: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(
            f"{self.url}/fire/{name}", dc=dc, node=node, service=service, tag=tag
        )
        async with self.client.put(url, json=data, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def list(
        self,
        name: Optional[str] = None,
        node: Optional[str] = None,
        service: Optional[str] = None,
        tag: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(
            f"{self.url}/list", name=name, node=node, service=service, tag=tag
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore
