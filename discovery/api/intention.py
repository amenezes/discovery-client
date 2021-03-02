import json

from discovery.api.abc import Api


class Intentions(Api):
    def __init__(self, endpoint: str = "/connect/intentions", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    def by_is_valid(self, by):
        if by.lower() not in ["source", "destination"]:
            raise ValueError('by must be: "source" or "destination"')
        return True

    async def create(self, data, dumps=json.dumps, **kwargs):
        response = await self.client.post(f"{self.url}", data=dumps(data), **kwargs)
        return response

    async def read(self, uuid, **kwargs):
        response = await self.client.get(f"{self.url}/{uuid}", **kwargs)
        return response

    async def list(self, **kwargs):
        response = await self.client.get(f"{self.url}", **kwargs)
        return response

    async def update(self, uuid, data, dumps=json.dumps, **kwargs):
        response = await self.client.put(
            f"{self.url}/{uuid}", data=dumps(data), **kwargs
        )
        return response

    async def delete(self, uuid, **kwargs):
        response = await self.client.delete(f"{self.url}/{uuid}", **kwargs)
        return response

    async def check(self, source, destination, **kwargs):
        response = await self.client.get(
            f"{self.url}/check?source={source}&destination={destination}", **kwargs
        )
        return response

    async def match(self, by, name, **kwargs):
        if self.by_is_valid(by):
            response = await self.client.get(
                f"{self.url}/match?by={by}&name={name}", **kwargs
            )
            return response
