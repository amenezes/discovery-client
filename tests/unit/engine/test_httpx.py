import pytest


@pytest.fixture
async def httpx_response(consul_httpx):
    response = await consul_httpx.client.get("https://httpbin.org/json")
    return response


@pytest.mark.asyncio
async def test_get(consul_httpx):
    response = await consul_httpx.client.get("https://httpbin.org/json")
    assert response.status == 200
    assert response.content_type == "application/json"


@pytest.mark.asyncio
async def test_json(httpx_response):
    response = await httpx_response.json()
    assert isinstance(response, dict)


@pytest.mark.asyncio
async def test_text(httpx_response):
    response = await httpx_response.text()
    assert isinstance(response, str)


@pytest.mark.asyncio
async def test_content(httpx_response):
    response = await httpx_response.content()
    assert isinstance(response, bytes)


@pytest.mark.asyncio
async def test_put(consul_httpx):
    response = await consul_httpx.client.put("https://httpbin.org/put")
    assert response.status == 200
    assert response.version == "1.1"


@pytest.mark.asyncio
async def test_delete(consul_httpx):
    response = await consul_httpx.client.delete("https://httpbin.org/delete")
    assert response.status == 200


@pytest.mark.asyncio
async def test_post(consul_httpx):
    response = await consul_httpx.client.post("https://httpbin.org/post")
    assert response.status == 200


def test_url(consul_httpx):
    assert consul_httpx.client.url == "http://localhost:8500"


def test_repr(consul_httpx):
    assert (
        str(consul_httpx)
        == "Consul(timeout=30.0, leader_id=None, engine=HTTPXEngine(host='localhost', port=8500, scheme='http'))"
    )


@pytest.mark.asyncio
async def test_response_repr(consul_httpx):
    response = await consul_httpx.client.get("https://httpbin.org/get")
    assert (
        str(response)
        == "Response(status=200, http_version='1.1', url='https://httpbin.org/get')"
    )
