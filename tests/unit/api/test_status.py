import pytest

from discovery import api


@pytest.fixture
@pytest.mark.asyncio
async def status(consul_api):
    return api.Status(client=consul_api)


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", ["127.0.0.1:8300"])
async def test_leader(status, expected):
    status.client.expected = expected
    response = await status.leader()
    resp = await response.json()
    assert resp == "127.0.0.1:8300"


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [["127.0.0.1:8300"]])
async def test_peers(status, expected):
    status.client.expected = expected
    response = await status.peers()
    resp = await response.json()
    assert resp == ["127.0.0.1:8300"]


def test_repr(status):
    assert f"{status}" == "Status(endpoint=/v1/status)"
