import pytest


@pytest.mark.asyncio
async def test_get(consul_httpx):
    response = await consul_httpx.client.get("https://httpbin.org/get")
    assert response.status == 200


@pytest.mark.asyncio
async def test_put(consul_httpx):
    response = await consul_httpx.client.put("https://httpbin.org/put")
    assert response.status == 200


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
