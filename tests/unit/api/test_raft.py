import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_read_configuration(raft, expected):
    raft.client.expected = expected
    response = await raft.read_configuration()
    assert response.status == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [["127.0.0.1:8300"]])
async def test_delete_peer(raft, expected):
    raft.client.expected = expected
    response = await raft.delete_peer(dc="dc1", address="127.0.0.1:8300")
    resp = await response.text()
    assert resp is not None
