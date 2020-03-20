import pytest

from discovery import api


@pytest.fixture
@pytest.mark.asyncio
async def snapshot(consul_api):
    return api.Snapshot(client=consul_api)


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_generate(snapshot, expected):
    snapshot.client.expected = expected
    response = await snapshot.generate()
    assert response.status == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_restore(snapshot, expected):
    snapshot.client.expected = expected
    snap = await snapshot.generate()
    data = await snap.read()
    response = await snapshot.restore(data=data)
    assert response.status == 200
