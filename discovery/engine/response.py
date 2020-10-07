from discovery.engine.base_response import BaseResponse


class Response:
    def __init__(self, response: BaseResponse):
        self._strategy = response

    @property
    def status(self):
        return self._strategy.status

    @property
    def url(self) -> str:
        return self._strategy.url

    @property
    def content_type(self) -> str:
        return self._strategy.content_type

    @property
    def version(self) -> str:
        return self._strategy.version

    @property
    def raw_response(self):
        return self._strategy.raw_response

    async def json(self):
        resp = await self._strategy.json()
        return resp

    async def text(self):
        resp = await self._strategy.text()
        return resp

    async def content(self) -> bytes:
        resp = await self._strategy.content()
        return resp
