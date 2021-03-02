import pytest

from discovery import api


@pytest.fixture
@pytest.mark.asyncio
async def snapshot(consul_api):
    return api.Snapshot(client=consul_api)


@pytest.mark.asyncio
async def test_generate(snapshot):
    snapshot.client.expected = 200
    response = await snapshot.generate()
    assert response.status == 200


@pytest.mark.asyncio
async def test_restore(snapshot):
    snapshot.client.expected = 200
    snap = await snapshot.generate()
    data = await snap.content()
    response = await snapshot.restore(data=data)
    assert response.status == 200
