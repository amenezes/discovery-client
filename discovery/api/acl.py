from typing import Optional

from discovery import api, log
from discovery.api.abc import Api


class Acl(Api):
    def __init__(
        self,
        auth_method=None,
        binding_rule=None,
        policy=None,
        role=None,
        token=None,
        endpoint: str = "/acl",
        **kwargs,
    ) -> None:
        super().__init__(endpoint=endpoint, **kwargs)
        self.auth_method = auth_method or api.AuthMethod(client=self.client)
        self.binding_rule = binding_rule or api.BindingRule(client=self.client)
        self.policy = policy or api.Policy(client=self.client)
        self.role = role or api.Role(client=self.client)
        self.token = token or api.Token(client=self.client)

    async def bootstrap(self) -> dict:
        async with self.client.put(f"{self.url}/bootstrap") as resp:
            return await resp.json()  # type: ignore

    async def replication(self, dc: Optional[str] = None, **kwargs) -> dict:
        url = self._prepare_request_url(f"{self.url}/replication", dc=dc)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def translate(self, data, **kwargs) -> dict:
        log.warning(
            "Deprecated - This endpoint was introduced in Consul 1.4.0 "
            "for migration from the previous ACL system. "
            "It will be removed in a future major Consul "
            "version when support for legacy ACLs is removed."
        )
        async with self.client.post(
            f"{self.url}/rules/translate", json=data, **kwargs
        ) as resp:
            return await resp.json()  # type: ignore
