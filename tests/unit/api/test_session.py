import pytest

from discovery import api
from tests.unit.setup import consul_api


def sample_payload():
    {
        "LockDelay": "15s",
        "Name": "my-service-lock",
        "Node": "foobar",
        "Checks": ["a", "b", "c"],
        "Behavior": "release",
        "TTL": "30s",
    }


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
@pytest.mark.asyncio
async def session(consul_api):
    return api.Session(client=consul_api)


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_create(session, expected):
    session.client.expected = expected
    response = await session.create(sample_payload())
    assert response.status == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_delete(session, expected):
    session.client.expected = expected
    response = await session.delete("adf4238a-882b-9ddc-4a9d-5b6758e4159e")
    assert response.status == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [sample_response()])
async def test_read(session, expected):
    session.client.expected = expected
    resp = await session.read("adf4238a-882b-9ddc-4a9d-5b6758e4159e")
    resp = await resp.json()
    assert resp == sample_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [sample_response()])
async def test_list_node_session(session, expected):
    session.client.expected = expected
    response = await session.list_node_session("raja-laptop-02")
    response = await response.json()
    assert response == sample_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [sample_response()])
async def test_list(session, expected):
    session.client.expected = expected
    response = await session.list()
    response = await response.json()
    assert response == sample_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [sample_response()])
async def test_renew(session, expected):
    session.client.expected = expected
    resp = await session.renew("adf4238a-882b-9ddc-4a9d-5b6758e4159e")
    resp = await resp.json()
    assert resp == sample_response()
