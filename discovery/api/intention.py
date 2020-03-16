from discovery.api.abc import Api


class Intentions(Api):
    def __init__(self, endpoint: str = "/connect/intentions", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    def by_is_valid(self, by):
        if by.lower() not in ["source", "destination"]:
            raise ValueError('by must be: "source" or "destination"')
        return True

    async def create(self, data, **kwargs):
        response = await self.client.post(f"{self.url}", params=kwargs, data=data)
        return response

    async def read(self, uuid, **kwargs):
        response = await self.client.get(f"{self.url}/{uuid}", params=kwargs)
        return response

    async def list(self, **kwargs):
        response = await self.client.get(f"{self.url}", params=kwargs)
        return response

    async def update(self, uuid, data, **kwargs):
        response = await self.client.put(f"{self.url}/{uuid}", params=kwargs, data=data)
        return response

    async def delete(self, uuid, **kwargs):
        response = await self.client.delete(f"{self.url}/{uuid}", params=kwargs)
        return response

    async def check(self, source, destination, **kwargs):
        response = await self.client.get(
            f"{self.url}/check?source={source}&destination={destination}", params=kwargs
        )
        return response

    async def match(self, by, name, **kwargs):
        if self.by_is_valid(by):
            response = await self.client.get(
                f"{self.url}/match?by={by}&name={name}", params=kwargs
            )
            return response
