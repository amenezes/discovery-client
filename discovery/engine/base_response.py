from abc import ABC


class BaseResponse(ABC):
    @property
    def status(self) -> int:
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

    async def content(self, *args, **kwargs) -> bytes:
        raise NotImplementedError

    def __repr__(self) -> str:
        *_, name = str(self.__class__).split(".")
        return f"{name[:-2]}(status={self.status}, http_version='{self.version}', url='{self.url}')"
