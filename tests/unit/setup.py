import aiohttp
import pytest

from discovery import api
from discovery.engine import AIOHTTPEngine


@pytest.fixture
async def aiohttp_client():
    session = aiohttp.ClientSession()
    yield AIOHTTPEngine(session)
    await session.close()


class ResponseMock:
    def __init__(self, expected=None):
        self.expected = expected
        self.status = expected

    async def json(self):
        return self.expected

    async def text(self):
        return self.expected

    async def read(self):
        return self.expected

    def status(self):
        return self.expected


class ApiMock:
    def __init__(self, expected=None):
        self.url = ""
        self.expected = expected

    async def get(self, *args, **kwargs):
        return ResponseMock(expected=self.expected)

    async def delete(self, *args, **kwargs):
        return ResponseMock(expected=self.expected)

    async def put(self, *args, **kwargs):
        return ResponseMock(expected=self.expected)

    async def post(self, *args, **kwargs):
        return ResponseMock(expected=self.expected)


@pytest.fixture
def consul_api(expected=None):
    return ApiMock(expected=expected)
