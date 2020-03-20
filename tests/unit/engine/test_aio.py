import pytest


@pytest.mark.asyncio
async def test_get(aiohttp_client):
    response = await aiohttp_client.get("https://httpbin.org/get")
    assert response.status == 200


@pytest.mark.asyncio
async def test_put(aiohttp_client):
    response = await aiohttp_client.put("https://httpbin.org/put")
    assert response.status == 200


@pytest.mark.asyncio
async def test_delete(aiohttp_client):
    response = await aiohttp_client.delete("https://httpbin.org/delete")
    assert response.status == 200


@pytest.mark.asyncio
async def test_post(aiohttp_client):
    response = await aiohttp_client.post("https://httpbin.org/post")
    assert response.status == 200


def test_url(aiohttp_client):
    assert aiohttp_client.url == "http://localhost:8500"
