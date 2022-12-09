from contextlib import asynccontextmanager

import pytest

from discovery import api
from discovery.client import Consul
from discovery.engine.httpx import HTTPXEngine


@pytest.fixture(scope="session")
def area(consul_api):
    return api.Area(client=consul_api)


@pytest.fixture(scope="session")
def consul_api(expected=None):
    yield ApiMock(expected=expected)


@pytest.fixture(scope="session")
def consul(consul_api):
    return Consul()


@pytest.fixture(scope="session")
def consul_httpx():
    return Consul(client=HTTPXEngine())


@pytest.fixture
async def segment(consul_api):
    return api.Segment(client=consul_api)


@pytest.fixture
async def raft(consul_api):
    return api.Raft(client=consul_api)


@pytest.fixture
async def license(consul_api):
    return api.License(client=consul_api)


@pytest.fixture
async def keyring(consul_api):
    return api.Keyring(client=consul_api)


@pytest.fixture
async def autopilot(consul_api):
    return api.AutoPilot(client=consul_api)


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

    @asynccontextmanager
    async def get(self, *args, **kwargs):
        yield ResponseMock(expected=self.expected)

    @asynccontextmanager
    async def delete(self, *args, **kwargs):
        yield ResponseMock(expected=self.expected)

    @asynccontextmanager
    async def put(self, *args, **kwargs):
        yield ResponseMock(expected=self.expected)

    @asynccontextmanager
    async def post(self, *args, **kwargs):
        yield ResponseMock(expected=self.expected)
