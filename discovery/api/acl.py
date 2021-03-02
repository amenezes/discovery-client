import json

from discovery import api, logging
from discovery.api.abc import Api
from discovery.engine.response import Response


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

    async def bootstrap(self) -> Response:
        response: Response = await self.client.put(f"{self.url}/bootstrap")
        return response

    async def replication(self, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}/replication", **kwargs)
        return response

    async def translate(self, data, dumps=json.dumps, **kwargs) -> Response:
        logging.warning(
            "Deprecated - This endpoint was introduced in Consul 1.4.0 "
            "for migration from the previous ACL system. "
            "It will be removed in a future major Consul "
            "version when support for legacy ACLs is removed."
        )
        response: Response = await self.client.post(
            f"{self.url}/rules/translate", data=dumps(data), **kwargs
        )
        return response
