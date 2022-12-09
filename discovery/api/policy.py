from typing import List, Optional

from discovery.api.abc import Api


class Policy(Api):
    def __init__(self, endpoint: str = "/acl/policy", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(
        self,
        name: str,
        description: str,
        rules: str,
        datacenters: List[str],
        namespace: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}", ns=ns)
        payload = dict(
            Name=name, Description=description, Rules=rules, Datacenters=datacenters
        )

        if namespace:
            payload.update({"Namespace": namespace})

        async with self.client.put(url, json=payload, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def read(self, policy_id: str, ns: Optional[str] = None, **kwargs) -> dict:
        url = self._prepare_request_url(f"{self.url}/{policy_id}", ns=ns)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def read_by_name(self, name: str, ns: Optional[str] = None, **kwargs) -> dict:
        url = self._prepare_request_url(f"{self.url}/name/{name}", ns=ns)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def update(
        self,
        policy_id: str,
        name: str,
        description: str,
        rules: str,
        datacenters: List[str],
        namespace: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs,
    ) -> dict:
        payload = dict(
            Name=name, Description=description, Rules=rules, Datacenters=datacenters
        )

        if namespace:
            payload.update({"Namespace": namespace})

        url = self._prepare_request_url(f"{self.url}/{policy_id}", ns=ns)
        async with self.client.put(url, json=payload, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def delete(self, policy_id: str, ns: Optional[str] = None, **kwargs) -> bool:
        url = self._prepare_request_url(f"{self.url}/{policy_id}", ns=ns)
        async with self.client.delete(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def list(self, ns: Optional[str] = None, **kwargs) -> List[dict]:
        url = self._prepare_request_url(
            f"{self.url.replace('policy', 'policies')}", ns=ns
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore
