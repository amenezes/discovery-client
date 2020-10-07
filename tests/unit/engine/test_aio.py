import pytest


@pytest.mark.asyncio
async def test_get(consul):
    response = await consul.client.get("https://httpbin.org/get")
    assert response.status == 200


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
