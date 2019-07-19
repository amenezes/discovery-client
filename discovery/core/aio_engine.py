import asyncio

import aiohttp

import attr

from discovery.core.base_engine import Engine


@attr.s(frozen=True)
class AioEngine(Engine):

    loop = attr.ib(default=asyncio.get_event_loop())
    _session = attr.ib(default=aiohttp.ClientSession())

    def get(self, url, **kwargs):
        return self._session.get(url, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self._session.put(url, **kwargs)

    def delete(self, url, **kwargs):
        return self._session.delete(url, **kwargs)

    def post(self, url, data=None, **kwargs):
        return self._session.post(url, **kwargs)
