from discovery.api.abc import Api


class BindingRule(Api):
    def __init__(self, endpoint: str = "/acl/binding-rule", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def create(self, data, **kwargs):
        response = await self.client.put(f"{self.url}", data=data, params=kwargs)
        return response

    async def read(self, role_id, **kwargs):
        response = await self.client.get(f"{self.url}/{role_id}", params=kwargs)
        return response

    async def update(self, data, role_id, **kwargs):
        response = await self.client.put(
            f"{self.url}/{role_id}", data=data, params=kwargs
        )
        return response

    async def delete(self, role_id, **kwargs):
        response = await self.client.delete(f"{self.url}/{role_id}", params=kwargs)
        return response

    async def list(self, **kwargs):
        response = await self.client.get(f"{self.url}", params=kwargs)
        return response
