from abc import ABC

from discovery.engine.abc import Engine


class Api(ABC):
    def __init__(
        self, client: Engine, endpoint: str = "/", version: str = "v1"
    ) -> None:
        self._client = client
        self.endpoint = endpoint
        self.version = version

    def __repr__(self) -> str:
        *_, name = str(self.__class__).split(".")
        return f"{name[:-2]}(endpoint={self.url})"

    @property
    def client(self) -> Engine:
        return self._client

    @property
    def url(self) -> str:
        return f"{self._client.url}/{self.version}{self.endpoint}"

    def _prepare_request_url(self, base_url: str, **kwargs) -> str:
        params = [
            f"{key.replace('_', '-')}={value}"
            for key, value in kwargs.items()
            if value is not None
        ]
        if len(params) > 0:
            return f"{base_url}?{'&'.join(params)}"
        return base_url
