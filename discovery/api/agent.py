from urllib.parse import quote_plus

from discovery import api
from discovery.api.abc import Api


class Agent(Api):
    def __init__(
        self,
        checks=None,
        connect=None,
        service=None,
        endpoint: str = "/agent",
        **kwargs,
    ):
        super().__init__(endpoint=endpoint, **kwargs)
        self.checks = checks or api.Checks(client=self.client)
        self.connect = connect or api.Connect(
            api.CA(client=self.client),
            api.Intentions(client=self.client),
            client=self.client,
        )
        self.service = service or api.Service(client=self.client)

    async def members(self, **kwargs):
        response = await self.client.get(f"{self.url}/members", params=kwargs)
        return response

    async def read_configuration(self, **kwargs):
        response = await self.client.get(f"{self.url}/self", params=kwargs)
        return response

    async def reload(self, **kwargs):
        response = await self.client.put(f"{self.url}/reload", params=kwargs)
        return response

    async def maintenance(self, enable=True, reason=None, **kwargs):
        reason = reason or ""
        response = await self.client.put(
            f"{self.url}/maintenance?enable={enable}&reason={quote_plus(reason)}",
            params=kwargs,
        )
        return response

    async def metrics(self, **kwargs):
        response = await self.client.get(f"{self.url}/metrics", params=kwargs)
        return response

    async def stream_logs(self, chunk_size=20, **kwargs):
        async with self.client.session.get(
            f"{self.url}/monitor", params=kwargs
        ) as resp:
            with open("/tmp/teste", "wb") as fd:
                while True:
                    chunk = await resp.content.read(chunk_size)
                    if not chunk:
                        break
                    fd.write(chunk)
        # response = await self.client.get(f"{self.url}/monitor", params=kwargs)
        # return response

    async def join(self, address, **kwargs):
        response = await self.client.put(f"{self.url}/join/{address}", params=kwargs)
        return response

    async def leave(self, **kwargs):
        response = await self.client.put(f"{self.url}/leave", params=kwargs)
        return response

    async def force_leave(self, node, **kwargs):
        response = await self.client.put(
            f"{self.url}/force-leave/{node}", params=kwargs
        )
        return response

    # async def service_health_by_name(self, name, **kwargs):
    #     response = await self.client.get(
    #         f"{self.url}/health/service/name/{name}", params=kwargs
    #     )
    #     return response

    # async def service_health_by_id(self, name, **kwargs):
    #     response = await self.client.get(
    #         f"{self.url}/health/service/id/{name}", params=kwargs
    #     )
    #     return response
