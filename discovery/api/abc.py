import abc

from discovery.engine.abc import Engine


class Api(abc.ABC):
    def __init__(
        self, client: Engine, endpoint: str = "/", version: str = "v1"
    ) -> None:
        self._client = client
        self.endpoint = endpoint
        self.version = version

    def __repr__(self) -> str:
        *_, name = str(self.__module__).split(".")
        return f"{name.title()}(endpoint={self.url})"

    @property
    def client(self) -> Engine:
        return self._client

    @property
    def url(self) -> str:
        return f"{self._client.url}/{self.version}{self.endpoint}"
