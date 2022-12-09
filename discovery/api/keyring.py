from typing import Optional

from discovery.api.abc import Api


class Keyring(Api):
    def __init__(self, endpoint: str = "/operator/keyring", **kwargs) -> None:
        super().__init__(endpoint=endpoint, **kwargs)

    async def list_keys(
        self,
        relay_factor: Optional[int] = None,
        local_only: Optional[bool] = None,
        **kwargs,
    ) -> dict:
        url = self._prepare_request_url(
            f"{self.url}", relay_factor=relay_factor, local_only=local_only
        )
        async with self.client.get(url, **kwargs) as resp:
            return await resp.json()  # type: ignore

    async def add_encryption_key(
        self, key: str, relay_factor: Optional[int] = None, **kwargs
    ) -> None:
        url = self._prepare_request_url(f"{self.url}", relay_factor=relay_factor)
        async with self.client.post(url, json=dict(Key=key), **kwargs):
            pass

    async def change_encryption_key(
        self, key: str, relay_factor: Optional[int] = None, **kwargs
    ) -> None:
        url = self._prepare_request_url(f"{self.url}", relay_factor=relay_factor)
        async with self.client.put(url, json=dict(Key=key), **kwargs):
            pass

    async def delete_encryption_key(
        self, key: str, relay_factor: Optional[int] = None, **kwargs
    ) -> None:
        url = self._prepare_request_url(f"{self.url}", relay_factor=relay_factor)
        async with self.client.delete(url, json=dict(Key=key), **kwargs):
            pass
