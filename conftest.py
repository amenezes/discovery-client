import pytest

from discovery import api
from discovery.client import Consul
from discovery.engine.httpx import HTTPXEngine


@pytest.fixture
def consul_api(expected=None):
    return ApiMock(expected=expected)


@pytest.fixture
def consul(consul_api):
    return Consul()


@pytest.fixture
def consul_httpx():
    return Consul(client=HTTPXEngine())


@pytest.fixture
@pytest.mark.asyncio
async def segment(consul_api):
    return api.Segment(client=consul_api)


@pytest.fixture
@pytest.mark.asyncio
async def raft(consul_api):
    return api.Raft(client=consul_api)


@pytest.fixture
@pytest.mark.asyncio
async def license(consul_api):
    return api.License(client=consul_api)


@pytest.fixture
@pytest.mark.asyncio
async def keyring(consul_api):
    return api.Keyring(client=consul_api)


@pytest.fixture
@pytest.mark.asyncio
async def autopilot(consul_api):
    return api.AutoPilot(client=consul_api)


@pytest.fixture
@pytest.mark.asyncio
def area(consul_api):
    return api.Area(client=consul_api)


class ResponseMock:
    def __init__(self, expected=None):
        self.expected = expected
        self.status = expected

    async def json(self):
        return self.expected

    async def text(self):
        return self.expected

    async def content(self):
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
