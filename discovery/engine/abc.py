import abc


class Engine(abc.ABC):
    def __init__(self, host="localhost", port=8500, scheme="http"):
        self._host = host
        self._port = port
        self._scheme = scheme

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
