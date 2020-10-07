from abc import ABC


class BaseResponse(ABC):
    @property
    def status(self):
        raise NotImplementedError

    @property
    def url(self) -> str:
        raise NotImplementedError

    @property
    def content_type(self) -> str:
        raise NotImplementedError

    @property
    def version(self) -> str:
        raise NotImplementedError

    @property
    def raw_response(self):
        raise NotImplementedError

    async def json(self):
        raise NotImplementedError

    async def text(self):
        raise NotImplementedError

    async def content(self) -> bytes:
        raise NotImplementedError
