from typing import List, Optional

from discovery.api.abc import Api


class Area(Api):
    def __init__(self, endpoint: str = "/operator/area", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create_network(
        self,
        peer_datacenter: str,
        retry_join: Optional[List[str]] = None,
        use_tls: bool = False,
        dc: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}", dc=dc)
        payload = dict(PeerDatacenter=peer_datacenter, UseTLS=use_tls)
        if retry_join:
            payload.update({"RetryJoin": retry_join})
        async with self.client.post(url, json=payload, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def list_network(self, dc: Optional[str] = None, **kwargs) -> dict:
        url = self._prepare_request_url(f"{self.url}", dc=dc)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def update_network(
        self,
        uuid: str,
        dc: Optional[str] = None,
        use_tls: bool = True,
        **kwargs,
    ) -> None:
        url = self._prepare_request_url(f"{self.url}/{uuid}", dc=dc)
        async with self.client.put(url, json=dict(UseTLS=use_tls), **kwargs):
            pass

    async def list_specific_network(self, uuid: str, dc: Optional[str] = None) -> dict:
        url = self._prepare_request_url(f"{self.url}/{uuid}", dc=dc)
        async with self.client.get(url) as resp:
            return await resp.json()  # type: ignore

    async def delete_network(
        self, uuid: str, dc: Optional[str] = None, **kwargs
    ) -> None:
        url = self._prepare_request_url(f"{self.url}/{uuid}", dc=dc)
        async with self.client.delete(url, **kwargs):
            pass

    async def join_network(
        self,
        uuid: str,
        data: List[str],
        dc: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}/{uuid}/join", dc=dc)
        async with self.client.put(url, json=data, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def list_network_members(
        self, uuid, dc: Optional[str] = None, **kwargs
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}/{uuid}/members", dc=dc)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore
