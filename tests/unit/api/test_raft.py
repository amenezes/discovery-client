import pytest


@pytest.mark.parametrize("expected", [dict])
async def test_read_configuration(raft, expected):
    raft.client.expected = {}
    response = await raft.read_configuration()
    assert isinstance(response, dict)


async def test_delete_peer_with_address(raft, mocker):
    spy = mocker.spy(raft.client, "delete")
    await raft.delete_peer(dc="dc1", address="127.0.0.1:8300")
    spy.assert_called_with("/v1/operator/raft/peer?address=127.0.0.1:8300&dc=dc1")


async def test_delete_peer_with_id(raft, mocker):
    spy = mocker.spy(raft.client, "delete")
    await raft.delete_peer(dc="dc1", peer_id="123-456-789")
    spy.assert_called_with("/v1/operator/raft/peer?id=123-456-789&dc=dc1")


async def test_delete_peer_error(raft):
    with pytest.raises(ValueError):
        await raft.delete_peer("123-456", "127.0.0.1:8300", "dc1")


async def test_delete_peer_without_query_param(raft, mocker):
    # spy = mocker.spy(raft.client, "delete")
    with pytest.raises(ValueError):
        await raft.delete_peer(dc="dc1")
    # spy.assert_called_with("/v1/operator/raft/peer?dc=dc1")
