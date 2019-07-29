from abc import ABC, abstractmethod

import attr


@attr.s(frozen=True, slots=True)
class Engine(ABC):

    host = attr.ib(type=str, default='localhost')
    port = attr.ib(type=int, default=8500)
    scheme = attr.ib(type=str, default='http')
    _url = attr.ib(type=str, default='{scheme}://{host}:{port}')

    @property
    def url(self):
        return self._url.format(
            scheme=self.scheme,
            host=self.host,
            port=self.port
        )

    @abstractmethod
    def get(self, url, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def put(self, url, data=None, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete(self, url, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def post(self, url, data=None, **kwargs):
        raise NotImplementedError
