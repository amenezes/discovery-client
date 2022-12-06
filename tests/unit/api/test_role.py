import pytest

from discovery import api


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
async def role(consul_api):
    return api.Role(client=consul_api)


@pytest.mark.parametrize("expected", [sample_response()])
async def test_create(role, expected):
    role.client.expected = expected
    response = await role.create(
        "example-role",
        "Showcases all input parameters",
        [{"ID": "783beef3-783f-f41f-7422-7087dc272765"}, {"Name": "node-read"}],
        [{"ServiceName": "web"}, {"ServiceName": "db", "Datacenters": ["dc1"]}],
        [{"NodeName": "node-1", "Datacenter": "dc2"}],
    )
    assert response == sample_response()


@pytest.mark.parametrize("expected", [sample_response()])
async def test_read_by_id(role, expected):
    role.client.expected = expected
    response = await role.read_by_id("aa770e5b-8b0b-7fcf-e5a1-8535fcc388b4")
    assert response == sample_response()


@pytest.mark.parametrize("expected", [sample_response()])
async def test_read_by_name(role, expected):
    role.client.expected = expected
    response = await role.read_by_name("example-role")
    assert response == sample_response()


@pytest.mark.parametrize("expected", [sample_response()])
async def test_update(role, expected):
    role.client.expected = expected
    response = await role.update(
        "8bec74a4-5ced-45ed-9c9d-bca6153490bb",
        "example-two",
        [{"Name": "node-read"}],
        [{"ServiceName": "db"}],
        [{"NodeName": "node-1", "Datacenter": "dc2"}],
    )
    assert response == sample_response()


async def test_delete(role):
    role.client.expected = True
    response = await role.delete("8f246b77-f3e1-ff88-5b48-8ec93abf3e05")
    assert response


@pytest.mark.parametrize("expected", [sample_list_response()])
async def test_list(role, expected):
    role.client.expected = expected
    response = await role.list()
    assert response == sample_list_response()
