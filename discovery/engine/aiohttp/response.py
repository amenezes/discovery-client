from discovery.engine.base_response import BaseResponse


class AIOHTTPResponse(BaseResponse):
    def __init__(self, response) -> None:
        self._response = response

    @property
    def status(self) -> int:
        return int(self._response.status)

    @property
    def url(self) -> str:
        return str(self._response.url)

    @property
    def content_type(self) -> str:
        return str(self._response.content_type)

    @property
    def version(self) -> str:
        http_version = self._response.version
        return f"{http_version.major}.{http_version.minor}"

    @property
    def raw_response(self):
        return self._response

    async def json(self):
        response = await self._response.json()
        return response

    async def text(self):
        response = await self._response.text()
        return response

    async def content(self, *args, **kwargs) -> bytes:
        response: bytes = await self._response.content.read(*args, **kwargs)
        return response
