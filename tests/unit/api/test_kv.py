import json

import pytest

from discovery import api


def sample_data():
    data = {"key": "value"}
    return json.dumps(data)


def read_response():
    return [
        {
            "CreateIndex": 100,
            "ModifyIndex": 200,
            "LockIndex": 200,
            "Key": "zip",
            "Flags": 0,
            "Value": "dGVzdA==",
            "Session": "adf4238a-882b-9ddc-4a9d-5b6758e4159e",
        }
    ]


@pytest.fixture
async def kv(consul_api):
    return api.Kv(client=consul_api)


async def test_create(kv):
    kv.client.expected = True

    response = await kv.create("test_key", sample_data())
    assert response


@pytest.mark.parametrize("expected", [read_response()])
async def test_read(kv, expected):
    kv.client.expected = expected
    response = await kv.read("test_key")
    assert response == read_response()


async def test_update(kv):
    kv.client.expected = True
    response = await kv.update("test_key", sample_data())
    assert response


async def test_delete(kv):
    kv.client.expected = True
    response = await kv.delete("test_key")
    assert response
