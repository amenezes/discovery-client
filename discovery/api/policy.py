from discovery.api.abc import Api


class Policy(Api):
    def __init__(self, endpoint: str = "/acl/policy", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(self, data, **kwargs):
        response = await self.client.put(f"{self.url}", data=data, **kwargs)
        return response

    async def read(self, policy_id, **kwargs):
        response = await self.client.get(f"{self.url}/{policy_id}", **kwargs)
        return response

    async def update(self, policy_id, data, **kwargs):
        response = await self.client.put(f"{self.url}/{policy_id}", data=data, **kwargs)
        return response

    async def delete(self, policy_id, **kwargs):
        response = await self.client.delete(f"{self.url}/{policy_id}", **kwargs)
        return response

    async def list(self, **kwargs):
        url = self.url.replace("policy", "policies")
        response = await self.client.get(f"{url}", **kwargs)
        return response
