import pytest

from discovery.engine.response import Response


@pytest.fixture
async def response(consul):
    async with consul.client.get("https://httpbin.org/json") as resp:
        yield resp


def test_resp_instance(response):
    assert isinstance(response, Response)


def test_status(response):
    assert response.status == 200


def test_url(response):
    assert response.url == "https://httpbin.org/json"


def test_content_type(response):
    assert response.content_type == "application/json"


async def test_version(response):
    assert response.version == "1.1"


async def test_json(response):
    content = await response.json()
    assert isinstance(content, dict)


async def test_text(response):
    content = await response.text()
    assert isinstance(content, str)


async def test_content(response):
    content = await response.content()
    assert isinstance(content, bytes)
