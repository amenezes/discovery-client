import logging
from contextlib import suppress

from discovery.engine.abc import Engine

logging.getLogger(__name__).addHandler(logging.NullHandler())


has_httpx = False
has_aiohttp = False

with suppress(ImportError):
    import aiohttp

    has_aiohttp = True
    import httpx

    has_httpx = True


class AioEngine(Engine):
    def __init__(self, session=None, **kwargs):
        super().__init__(**kwargs)
        self._session = session

    async def get(self, *args, **kwargs):
        response = await self._session.get(*args, **kwargs)
        return response

    async def put(self, *args, **kwargs):
        response = await self._session.put(*args, **kwargs)
        return response

    async def delete(self, *args, **kwargs):
        response = await self._session.delete(*args, **kwargs)
        return response

    async def post(self, *args, **kwargs):
        response = await self._session.post(*args, **kwargs)
        return response

    async def __aexit__(self, *args, **kwargs):
        await self._session.close()


async def aiohttp_session(*args, **kwargs):
    if not has_aiohttp:
        raise ModuleNotFoundError("aiohttp module not found!")
    return aiohttp.ClientSession(*args, **kwargs)


async def httpx_client(*args, **kwargs):
    if not has_httpx:
        raise ModuleNotFoundError("httpx module not found!")
    return httpx.AsyncClient(*args, **kwargs)
