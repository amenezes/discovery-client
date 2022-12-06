from typing import Optional

from discovery.api.abc import Api


class Raft(Api):
    def __init__(self, endpoint: str = "/operator/raft", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def read_configuration(
        self, dc: Optional[str] = None, stale: Optional[bool] = None, **kwargs
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}/configuration", dc=dc, stale=stale)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def delete_peer(
        self,
        peer_id: Optional[str] = None,
        address: Optional[str] = None,
        dc: Optional[str] = None,
        **kwargs,
    ) -> None:
        if peer_id and address:
            raise ValueError("specify only peer_id or address field")

        if peer_id:
            query_param = {"id": peer_id}
        elif address:
            query_param = {"address": address}
        else:
            raise ValueError("peer_id or address are required field")
        url = self._prepare_request_url(f"{self.url}/peer", **query_param, dc=dc)
        async with self.client.delete(url, **kwargs):
            pass
