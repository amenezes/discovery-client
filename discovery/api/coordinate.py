from typing import Optional

from discovery.api.abc import Api


class Coordinate(Api):
    def __init__(self, endpoint: str = "/coordinate", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def read_wan(self, **kwargs) -> dict:
        async with self.client.get(f"{self.url}/datacenters", **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def read_lan_for_all_nodes(
        self, dc: Optional[str] = None, segment: Optional[str] = None, **kwargs
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}/nodes", dc=dc, segment=segment)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def read_lan_for_node(
        self,
        node_name: str,
        dc: Optional[str] = None,
        segment: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(
            f"{self.url}/node/{node_name}", dc=dc, segment=segment
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def update_lan_for_node(
        self, data: dict, dc: Optional[str] = None, **kwargs
    ) -> None:
        url = self._prepare_request_url(f"{self.url}/update", dc=dc)
        async with self.client.put(url, json=data, **kwargs):
            pass
