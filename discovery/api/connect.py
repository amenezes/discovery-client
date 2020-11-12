import json

from discovery import api
from discovery.api.abc import Api
from discovery.engine.response import Response


class Connect(Api):
    def __init__(
        self, ca=None, intentions=None, endpoint: str = "/agent/connect", **kwargs
    ) -> None:
        super().__init__(endpoint=endpoint, **kwargs)
        self.ca = ca or api.CA(client=self.client)
        self.intentions = intentions or api.Intentions(client=self.client)

    async def authorize(
        self, target, client_cert_uri, client_cert_serial, namespace=None
    ) -> Response:
        data = dict(
            Target=target,
            ClientCertURI=client_cert_uri,
            ClientCertSerial=client_cert_serial,
        )
        if namespace:
            data.update({"Namespace": namespace})
        response: Response = await self.client.post(
            f"{self.url}/authorize", data=json.dumps(data)
        )
        return response

    async def ca_roots(self) -> Response:
        response: Response = await self.client.get(f"{self.url}/ca/roots")
        return response

    async def leaf_certificate(self, service: str) -> Response:
        response: Response = await self.client.get(f"{self.url}/ca/leaf/{service}")
        return response
