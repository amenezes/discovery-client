import pytest

from discovery import api


def sample_response():
    return {
        "ID": "e359bd81-baca-903e-7e64-1ccd9fdc78f5",
        "Name": "node-read",
        "Description": "Grants read access to all node information",
        "Rules": "node_prefix '' { policy = 'read'}",
        "Datacenters": ["dc1"],
        "Hash": "OtZUUKhInTLEqTPfNSSOYbRiSBKm3c4vI2p6MxZnGWc=",
        "CreateIndex": 14,
        "ModifyIndex": 14,
    }


def sample_list_response():
    return [
        {
            "CreateIndex": 4,
            "Datacenters": None,
            "Description": "Builtin Policy that grants unlimited access",
            "Hash": "swIQt6up+s0cV4kePfJ2aRdKCLaQyykF4Hl1Nfdeumk=",
            "ID": "00000000-0000-0000-0000-000000000001",
            "ModifyIndex": 4,
            "Name": "global-management",
        },
        {
            "CreateIndex": 14,
            "Datacenters": ["dc1"],
            "Description": "Grants read access to all node information",
            "Hash": "OtZUUKhInTLEqTPfNSSOYbRiSBKm3c4vI2p6MxZnGWc=",
            "ID": "e359bd81-baca-903e-7e64-1ccd9fdc78f5",
            "ModifyIndex": 14,
            "Name": "node-read",
        },
    ]


@pytest.fixture
async def policy(consul_api):
    return api.Policy(client=consul_api)


@pytest.mark.parametrize("expected", [sample_response()])
async def test_create(policy, expected):
    policy.client.expected = expected
    response = await policy.create(
        "node-read",
        "Grants read access to all node information",
        'node_prefix "" { policy = "read"}',
        ["dc1"],
    )
    assert response == sample_response()


@pytest.mark.parametrize("expected", [sample_response()])
async def test_read(policy, expected):
    policy.client.expected = expected
    response = await policy.read("e359bd81-baca-903e-7e64-1ccd9fdc78f5")
    assert response == sample_response()


@pytest.mark.parametrize("expected", [sample_response()])
async def test_update(policy, expected):
    policy.client.expected = expected
    response = await policy.update(
        "c01a1f82-44be-41b0-a686-685fb6e0f485",
        "register-app-service",
        "Grants write permissions necessary to register the 'app' service",
        'service "app" { policy = "write"}',
        ["dc1"],
    )
    assert response == sample_response()


async def test_delete(policy):
    policy.client.expected = True
    response = await policy.delete("e359bd81-baca-903e-7e64-1ccd9fdc78f5")
    assert response


@pytest.mark.parametrize("expected", [sample_list_response()])
async def test_list(policy, expected):
    policy.client.expected = expected
    response = await policy.list()
    assert response == sample_list_response()
