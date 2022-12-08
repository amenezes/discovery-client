import pytest


@pytest.fixture
async def httpx_response(consul_httpx):
    async with consul_httpx.client.get("https://httpbin.org/json") as response:
        yield response


async def test_get(httpx_response):
    response = httpx_response
    assert response.status == 200
    assert response.content_type == "application/json"


async def test_json(httpx_response):
    response = await httpx_response.json()
    assert isinstance(response, dict)


async def test_text(httpx_response):
    content = await httpx_response.text()
    assert isinstance(content, str)


async def test_content(httpx_response):
    response = await httpx_response.content()
    assert isinstance(response, bytes)


async def test_put(consul_httpx):
    async with consul_httpx.client.put("https://httpbin.org/put") as response:
        assert response.status == 200
        assert response.version == "1.1"


async def test_delete(consul_httpx):
    async with consul_httpx.client.delete("https://httpbin.org/delete") as response:
        assert response.status == 200


async def test_post(consul_httpx):
    async with consul_httpx.client.post("https://httpbin.org/post") as response:
        assert response.status == 200


def test_url(consul_httpx):
    assert consul_httpx.client.url == "http://localhost:8500"


def test_repr(consul_httpx):
    assert (
        str(consul_httpx)
        == "Consul(engine=HTTPXEngine(host='localhost', port=8500, scheme='http'))"
    )


async def test_response_repr(consul_httpx):
    async with consul_httpx.client.get("https://httpbin.org/get") as response:
        assert (
            str(response)
            == "Response(status=200, http_version='1.1', url='https://httpbin.org/get')"
        )
