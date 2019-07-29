import attr

from discovery.core.engine.base import Engine

import requests


@attr.s(frozen=True, slots=True)
class StandardEngine(Engine):

    _session = attr.ib(default=requests.Session())

    def get(self, url, **kwargs):
        return self._session.get(url, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self._session.put(url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self._session.delete(url, **kwargs)

    def post(self, url, data=None, **kwargs):
        return self._session.post(url, data=data, **kwargs)
