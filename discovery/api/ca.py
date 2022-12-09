from typing import Dict, Optional

from discovery.api.abc import Api


class CA(Api):
    def __init__(self, endpoint: str = "/connect/ca", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def list_root_certificates(
        self, pem: Optional[bool] = None, **kwargs
    ) -> dict:
        url = self._prepare_request_url(f"{self.url}/roots", pem=pem)
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def configuration(self, **kwargs) -> dict:
        async with self.client.get(f"{self.url}/configuration", **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def update_configuration(
        self,
        provider: str,
        config: Dict[str, str],
        force_without_cross_signing: bool = False,
        **kwargs,
    ) -> None:
        payload = dict(Provider=provider, Config=config)

        if force_without_cross_signing:
            payload.update({"ForceWithoutCrossSigning": force_without_cross_signing})  # type: ignore

        async with self.client.put(f"{self.url}/configuration", json=payload, **kwargs):
            pass
