import json

import pytest

from discovery import api
from tests.unit.setup import consul_api


def sample_list_response(*args, **kwargs):
    return [
        {
            "ID": "5e52a099-4c90-c067-5478-980f06be9af5",
            "Name": "node-read",
            "Description": "",
            "Policies": [
                {"ID": "783beef3-783f-f41f-7422-7087dc272765", "Name": "node-read"}
            ],
            "Hash": "K6AbfofgiZ1BEaKORBloZf7WPdg45J/PipHxQiBlK1U=",
            "CreateIndex": 50,
            "ModifyIndex": 50,
        },
        {
            "ID": "aa770e5b-8b0b-7fcf-e5a1-8535fcc388b4",
            "Name": "example-role",
            "Description": "Showcases all input parameters",
            "Policies": [
                {"ID": "783beef3-783f-f41f-7422-7087dc272765", "Name": "node-read"}
            ],
            "ServiceIdentities": [
                {"ServiceName": "web"},
                {"ServiceName": "db", "Datacenters": ["dc1"]},
            ],
            "Hash": "mBWMIeX9zyUTdDMq8vWB0iYod+mKBArJoAhj6oPz3BI=",
            "CreateIndex": 57,
            "ModifyIndex": 57,
        },
    ]


def sample_token_response(*args, **kwargs):
    return {
        "ID": "8bec74a4-5ced-45ed-9c9d-bca6153490bb",
        "Name": "example-two",
        "Policies": [
            {"ID": "783beef3-783f-f41f-7422-7087dc272765", "Name": "node-read"}
        ],
        "ServiceIdentities": [{"ServiceName": "db"}],
        "Hash": "OtZUUKhInTLEqTPfNSSOYbRiSBKm3c4vI2p6MxZnGWc=",
        "CreateIndex": 14,
        "ModifyIndex": 28,
    }


def sample_payload(*args, **kwargs):
    return json.dumps(
        {
            "ID": "8bec74a4-5ced-45ed-9c9d-bca6153490bb",
            "Name": "example-two",
            "Policies": [{"Name": "node-read"}],
            "ServiceIdentities": [{"ServiceName": "db"}],
        }
    )


@pytest.fixture
@pytest.mark.asyncio
async def token(consul_api):
    return api.Token(client=consul_api)


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [sample_token_response()])
async def test_create(token, expected):
    token.client.expected = expected
    response = await token.create(sample_payload())
    response = await response.json()
    assert response == sample_token_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [sample_token_response()])
async def test_read_by_id(token, expected):
    token.client.expected = expected
    response = await token.read_by_id("8bec74a4-5ced-45ed-9c9d-bca6153490bb")
    response = await response.json()
    assert response == sample_token_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [sample_token_response()])
async def test_read_by_name(token, expected):
    token.client.expected = expected
    response = await token.read_by_name("example-two")
    response = await response.json()
    assert response == sample_token_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [sample_token_response()])
async def test_update(token, expected):
    token.client.expected = expected
    response = await token.update(
        "8f246b77-f3e1-ff88-5b48-8ec93abf3e05", sample_payload()
    )
    response = await response.json()
    assert response == sample_token_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_delete(token, expected):
    token.client.expected = expected
    response = await token.delete("8f246b77-f3e1-ff88-5b48-8ec93abf3e05")
    assert response.status == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [sample_list_response()])
async def test_list(token, expected):
    token.client.expected = expected
    response = await token.list()
    response = await response.json()
    assert response == sample_list_response()
