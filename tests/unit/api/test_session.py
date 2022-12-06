import pytest

from discovery import api


def sample_response():
    return [
        {
            "ID": "adf4238a-882b-9ddc-4a9d-5b6758e4159e",
            "Name": "test-session",
            "Node": "raja-laptop-02",
            "Checks": ["serfHealth"],
            "LockDelay": 1.5e10,
            "Behavior": "release",
            "TTL": "30s",
            "CreateIndex": 1086449,
            "ModifyIndex": 1086449,
        }
    ]


@pytest.fixture
async def session(consul_api):
    return api.Session(client=consul_api)


async def test_create(session):
    await session.create("my-service-lock", "foobar", ["a", "b", "c"], ttl="30s")


async def test_delete(session):
    session.client.expected = True
    response = await session.delete("adf4238a-882b-9ddc-4a9d-5b6758e4159e")
    assert response


@pytest.mark.parametrize("expected", [sample_response()])
async def test_read(session, expected):
    session.client.expected = expected
    resp = await session.read("adf4238a-882b-9ddc-4a9d-5b6758e4159e")
    assert resp == sample_response()


@pytest.mark.parametrize("expected", [sample_response()])
async def test_list_sessions_for_node(session, expected):
    session.client.expected = expected
    response = await session.list_sessions_for_node("node-abcd1234")
    assert response == sample_response()


@pytest.mark.parametrize("expected", [sample_response()])
async def test_list(session, expected):
    session.client.expected = expected
    response = await session.list()
    assert response == sample_response()


@pytest.mark.parametrize("expected", [sample_response()])
async def test_renew(session, expected):
    session.client.expected = expected
    resp = await session.renew("adf4238a-882b-9ddc-4a9d-5b6758e4159e")
    assert resp == sample_response()
