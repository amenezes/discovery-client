import aiohttp
import pytest


@pytest.mark.asyncio
async def test_get(consul):
    response = await consul.client.get("https://httpbin.org/get")
    assert response.status == 200
    assert response.version == "1.1"


@pytest.mark.asyncio
async def test_put(consul):
    response = await consul.client.put("https://httpbin.org/put")
    assert response.status == 200


@pytest.mark.asyncio
async def test_delete(consul):
    response = await consul.client.delete("https://httpbin.org/delete")
    assert response.status == 200


@pytest.mark.asyncio
async def test_post(consul):
    response = await consul.client.post("https://httpbin.org/post")
    assert response.status == 200


def test_url(consul):
    assert consul.client.url == "http://localhost:8500"


def test_repr(consul):
    assert (
        str(consul)
        == "Consul(timeout=30, leader_active_id=None, engine=AIOHTTPEngine(host='localhost', port=8500, scheme='http'))"
    )


@pytest.mark.asyncio
async def test_response_repr(consul):
    response = await consul.client.get("https://httpbin.org/get")
    assert (
        str(response)
        == "Response(status=200, http_version='1.1', url='https://httpbin.org/get')"
    )


@pytest.mark.asyncio
async def test_raw_response(consul):
    response = await consul.client.get("https://httpbin.org/get")
    assert isinstance(response.raw_response, aiohttp.client_reqrep.ClientResponse)
