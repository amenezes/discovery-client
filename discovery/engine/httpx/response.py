try:
    from httpx import Response
except ModuleNotFoundError:
    Response = None  # type: ignore

from discovery.engine.base_response import BaseResponse


class HTTPXResponse(BaseResponse):
    def __init__(self, response: Response) -> None:
        self._strategy = response

    @property
    def status(self) -> int:
        return self._strategy.status_code

    @property
    def url(self) -> str:
        return str(self._strategy.url)

    @property
    def content_type(self) -> str:
        return str(self._strategy.headers["Content-Type"])

    @property
    def version(self) -> str:
        _, http_version = self._strategy.http_version.split("/")
        return f"{http_version}"

    @property
    def raw_strategy(self):
        return self._strategy

    async def json(self):
        return self._strategy.json()

    async def text(self) -> str:
        return self._strategy.text

    async def content(self, *args, **kwargs) -> bytes:
        return bytes(self._strategy.content)
