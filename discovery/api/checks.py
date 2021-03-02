import json

from discovery.api.abc import Api
from discovery.engine.response import Response


class Checks(Api):
    def __init__(self, endpoint: str = "/agent/check", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def checks(self, **kwargs) -> Response:
        response: Response = await self.client.get(f"{self.url}s", **kwargs)
        return response

    async def register(self, data, dumps=json.dumps, **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}/register", data=dumps(data), **kwargs
        )
        return response

    async def deregister(self, check_id, **kwargs):
        response: Response = await self.client.put(
            f"{self.url}/deregister/{check_id}", **kwargs
        )
        return response

    async def check_pass(self, check_id, notes="", **kwargs):
        response: Response = await self.client.put(
            f"{self.url}/pass/{check_id}", data=notes, **kwargs
        )
        return response

    async def check_warn(self, check_id, notes="", **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}/warn/{check_id}", data=notes, **kwargs
        )
        return response

    async def check_fail(self, check_id, notes="", **kwargs) -> Response:
        response: Response = await self.client.put(
            f"{self.url}/fail/{check_id}", data=notes, **kwargs
        )
        return response

    async def check_update(self, check_id, status, output="", **kwargs) -> Response:
        status = str(status).lower()
        if status not in ["passing", "warning", "critical"]:
            raise ValueError('Valid values are "passing", "warning", and "critical"')
        data = dict(status=status, output=output)
        response: Response = await self.client.put(
            f"{self.url}/update/{check_id}", data=json.dumps(data), **kwargs
        )
        return response
