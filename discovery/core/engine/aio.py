import aiohttp

import attr

from discovery.core.engine.base import Engine


@attr.s(frozen=True, slots=True)
class AioEngine(Engine):

    _session = attr.ib(default=aiohttp.ClientSession())

    async def get(self, url, **kwargs):
        response = await self._session.get(url, **kwargs)
        return response

    async def put(self, url, data=None, **kwargs):
        response = await self._session.put(url, data=data, **kwargs)
        return response

    async def delete(self, url, **kwargs):
        response = await self._session.delete(url, **kwargs)
        return response

    async def post(self, url, data=None, **kwargs):
        response = await self._session.post(url, data=data, **kwargs)
        return response
