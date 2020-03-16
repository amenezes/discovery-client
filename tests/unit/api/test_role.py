import pytest

from discovery import api
from tests.unit.setup import consul_api


def sample_payload():
    return {
        "Name": "example-role",
        "Description": "Showcases all input parameters",
        "Policies": [
            {"ID": "783beef3-783f-f41f-7422-7087dc272765"},
            {"Name": "node-read"},
        ],
        "ServiceIdentities": [
            {"ServiceName": "web"},
            {"ServiceName": "db", "Datacenters": ["dc1"]},
        ],
    }


def sample_response():
    return {
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
    }


def sample_list_response():
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


@pytest.fixture
@pytest.mark.asyncio
async def role(consul_api):
    return api.Role(client=consul_api)


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [sample_response()])
async def test_create(role, expected):
    role.client.expected = expected
    response = await role.create(sample_payload())
    response = await response.json()
    assert response == sample_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [sample_response()])
async def test_read_by_id(role, expected):
    role.client.expected = expected
    response = await role.read_by_id("aa770e5b-8b0b-7fcf-e5a1-8535fcc388b4")
    response = await response.json()
    assert response == sample_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [sample_response()])
async def test_read_by_name(role, expected):
    role.client.expected = expected
    response = await role.read_by_name("example-role")
    response = await response.json()
    assert response == sample_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [sample_response()])
async def test_update(role, expected):
    role.client.expected = expected
    response = await role.update(
        "8bec74a4-5ced-45ed-9c9d-bca6153490bb", sample_payload()
    )
    response = await response.json()
    assert response == sample_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_delete(role, expected):
    role.client.expected = expected
    response = await role.delete("8f246b77-f3e1-ff88-5b48-8ec93abf3e05")
    assert response.status == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [sample_list_response()])
async def test_list(role, expected):
    role.client.expected = expected
    response = await role.list()
    response = await response.json()
    assert response == sample_list_response()
