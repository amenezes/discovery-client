import abc
import os


class Engine(abc.ABC):
    def __init__(self, host: str = "localhost", port: int = 8500, scheme: str = "http"):
        self._host = str(os.getenv("CONSUL_HOST", host))
        self._port = int(os.getenv("CONSUL_PORT", port))
        self._scheme = str(os.getenv("CONSUL_SCHEMA", scheme))

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def scheme(self):
        return self._scheme

    @property
    def url(self):
        return f"{self.scheme}://{self.host}:{self.port}"

    async def get(self, *args, **kwargs):
        raise NotImplementedError

    async def put(self, *args, **kwargs):
        raise NotImplementedError

    async def delete(self, *args, **kwargs):
        raise NotImplementedError

    async def post(self, *args, **kwargs):
        raise NotImplementedError

    def __repr__(self):
        *_, name = str(self.__class__).split(".")
        return f"{name[:-2]}(host='{self._host}', port={self._port}, scheme='{self._scheme}')"
