import json

from discovery.api.abc import Api


class Checks(Api):
    def __init__(self, endpoint: str = "/agent/check", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    async def checks(self, **kwargs):
        response = await self.client.get(f"{self.url}s", params=kwargs)
        return response

    async def register(self, data, **kwargs):
        response = await self.client.put(
            f"{self.url}/register", data=data, params=kwargs
        )
        return response

    async def deregister(self, check_id, **kwargs):
        response = await self.client.put(
            f"{self.url}/deregister/{check_id}", params=kwargs
        )
        return response

    async def check_pass(self, check_id, notes="", **kwargs):
        response = await self.client.put(
            f"{self.url}/pass/{check_id}", data=notes, params=kwargs
        )
        return response

    async def check_warn(self, check_id, notes="", **kwargs):
        response = await self.client.put(
            f"{self.url}/warn/{check_id}", data=notes, params=kwargs
        )
        return response

    async def check_fail(self, check_id, notes="", **kwargs):
        response = await self.client.put(
            f"{self.url}/fail/{check_id}", data=notes, params=kwargs
        )
        return response

    async def check_update(self, check_id, status, output="", **kwargs):
        status = str(status).lower()
        if status not in ["passing", "warning", "critical"]:
            raise ValueError('Valid values are "passing", "warning", and "critical"')
        data = dict(status=status, output=output)
        response = await self.client.put(
            f"{self.url}/update/{check_id}", data=json.dumps(data), params=kwargs
        )
        return response
