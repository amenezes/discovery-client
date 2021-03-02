import abc
import os
from functools import cached_property


class Engine(abc.ABC):
    def __init__(self, host: str = "localhost", port: int = 8500, scheme: str = "http"):
        self._host = os.getenv("CONSUL_HOST", host)
        self._port = int(os.getenv("CONSUL_PORT", port))
        self._scheme = os.getenv("CONSUL_SCHEMA", scheme)

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def scheme(self) -> str:
        return self._scheme

    @cached_property
    def url(self) -> str:
        return f"{self.scheme}://{self.host}:{self.port}"

    async def get(self, *args, **kwargs):
        raise NotImplementedError

    async def put(self, *args, **kwargs):
        raise NotImplementedError

    async def delete(self, *args, **kwargs):
        raise NotImplementedError

    async def post(self, *args, **kwargs):
        raise NotImplementedError

    def __repr__(self) -> str:
        *_, name = str(self.__class__).split(".")
        return (
            f"{name[:-2]}(host='{self.host}', port={self.port}, scheme='{self.scheme}')"
        )
