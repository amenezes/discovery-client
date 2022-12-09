from typing import Optional

from discovery import api
from discovery.api.abc import Api


class Connect(Api):
    def __init__(
        self, ca=None, intentions=None, endpoint: str = "/agent/connect", **kwargs
    ) -> None:
        super().__init__(endpoint=endpoint, **kwargs)
        self.ca = ca or api.CA(client=self.client)
        self.intentions = intentions or api.Intentions(client=self.client)

    async def authorize(
        self,
        target: str,
        client_cert_uri: str,
        client_cert_serial: str,
        ns: Optional[str] = None,
        namespace: Optional[str] = None,
        **kwargs,
    ) -> dict:
        payload = dict(
            Target=target,
            ClientCertURI=client_cert_uri,
            ClientCertSerial=client_cert_serial,
        )
        if namespace:
            payload.update({"Namespace": namespace})
        url = self._prepare_request_url(f"{self.url}/authorize", ns=ns)
        async with self.client.post(url, json=payload, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def ca_roots(self, **kwargs) -> dict:
        async with self.client.get(f"{self.url}/ca/roots", **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def leaf_certificate(self, service: str, ns: Optional[str] = None) -> dict:
        url = self._prepare_request_url(f"{self.url}/ca/leaf/{service}", ns=ns)
        async with self.client.get(url) as resp:
            return await resp.json()  # type: ignore
