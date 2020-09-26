import json

import pytest

from discovery import api


def sample_payload():
    return json.dumps(
        {
            "SourceName": "web",
            "DestinationName": "db",
            "SourceType": "consul",
            "Action": "allow",
        }
    )


def sample_response():
    return {"ID": "8f246b77-f3e1-ff88-5b48-8ec93abf3e05"}


def sample_intent_response():
    return {
        "ID": "e9ebc19f-d481-42b1-4871-4d298d3acd5c",
        "Description": "",
        "SourceNS": "default",
        "SourceName": "web",
        "DestinationNS": "default",
        "DestinationName": "db",
        "SourceType": "consul",
        "Action": "allow",
        "DefaultAddr": "",
        "DefaultPort": 0,
        "Meta": {},
        "Precedence": 9,
        "CreatedAt": "2018-05-21T16:41:27.977155457Z",
        "UpdatedAt": "2018-05-21T16:41:27.977157724Z",
        "CreateIndex": 11,
        "ModifyIndex": 11,
    }


def sample_intentions_response():
    return [sample_response]


def list_match_response():
    return {
        "web": [
            {
                "ID": "ed16f6a6-d863-1bec-af45-96bbdcbe02be",
                "Description": "",
                "SourceNS": "default",
                "SourceName": "web",
                "DestinationNS": "default",
                "DestinationName": "db",
                "SourceType": "consul",
                "Action": "deny",
                "DefaultAddr": "",
                "DefaultPort": 0,
                "Meta": {},
                "CreatedAt": "2018-05-21T16:41:33.296693825Z",
                "UpdatedAt": "2018-05-21T16:41:33.296694288Z",
                "CreateIndex": 12,
                "ModifyIndex": 12,
            },
            {
                "ID": "e9ebc19f-d481-42b1-4871-4d298d3acd5c",
                "Description": "",
                "SourceNS": "default",
                "SourceName": "web",
                "DestinationNS": "default",
                "DestinationName": "*",
                "SourceType": "consul",
                "Action": "allow",
                "DefaultAddr": "",
                "DefaultPort": 0,
                "Meta": {},
                "CreatedAt": "2018-05-21T16:41:27.977155457Z",
                "UpdatedAt": "2018-05-21T16:41:27.977157724Z",
                "CreateIndex": 11,
                "ModifyIndex": 11,
            },
        ]
    }


def check_response():
    return {"Allowed": True}


def update_payload():
    return json.dumps(
        {
            "SourceName": "web",
            "DestinationName": "other-db",
            "SourceType": "consul",
            "Action": "allow",
        }
    )


@pytest.fixture
@pytest.mark.asyncio
async def intention(consul_api):
    return api.Intentions(client=consul_api)


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [sample_response()])
async def test_create_intention(intention, expected):
    intention.client.expected = expected
    response = await intention.create(sample_payload())
    response = await response.json()
    assert response == sample_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [sample_intent_response()])
async def test_read(intention, expected):
    intention.client.expected = expected
    response = await intention.read("e9ebc19f-d481-42b1-4871-4d298d3acd5c")
    response = await response.json()
    assert response == sample_intent_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [sample_intentions_response()])
async def test_list(intention, expected):
    intention.client.expected = expected
    response = await intention.list()
    response = await response.json()
    assert response == sample_intentions_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_update(intention, expected):
    intention.client.expected = expected
    response = await intention.update(
        "e9ebc19f-d481-42b1-4871-4d298d3acd5c", update_payload()
    )
    assert response.status == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_delete(intention, expected):
    intention.client.expected = expected
    response = await intention.delete("e9ebc19f-d481-42b1-4871-4d298d3acd5c")
    assert response.status == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [check_response()])
async def test_check(intention, expected):
    intention.client.expected = expected
    response = await intention.check("web", "db")
    response = await response.json()
    assert response == check_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [list_match_response()])
async def test_match_success(intention, expected):
    intention.client.expected = expected
    response = await intention.match("source", "web")
    response = await response.json()
    assert response == list_match_response()


@pytest.mark.asyncio
async def test_match_invalid(intention):
    with pytest.raises(ValueError):
        await intention.match("origin", "web")
