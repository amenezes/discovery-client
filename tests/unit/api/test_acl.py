import pytest

from discovery import api


def bootstrap_response():
    return {
        "ID": "527347d3-9653-07dc-adc0-598b8f2b0f4d",
        "AccessorID": "b5b1a918-50bc-fc46-dec2-d481359da4e3",
        "SecretID": "527347d3-9653-07dc-adc0-598b8f2b0f4d",
        "Description": "Bootstrap Token (Global Management)",
        "Policies": [
            {"ID": "00000000-0000-0000-0000-000000000001", "Name": "global-management"}
        ],
        "Local": False,
        "CreateTime": "2018-10-24T10:34:20.843397-04:00",
        "Hash": "oyrov6+GFLjo/KZAfqgxF/X4J/3LX0435DOBy9V22I0=",
        "CreateIndex": 12,
        "ModifyIndex": 12,
    }


def replication_response():
    return {
        "Enabled": True,
        "Running": True,
        "SourceDatacenter": "dc1",
        "ReplicationType": "tokens",
        "ReplicatedIndex": 1976,
        "ReplicatedTokenIndex": 2018,
        "LastSuccess": "2018-11-03T06:28:58Z",
        "LastError": "2016-11-03T06:28:28Z",
    }


def translate_payload():
    return 'agent "" {policy = "read"}'


def translate_response():
    return 'agent_prefix "" {policy = "read"}'


@pytest.fixture
async def acl(consul_api):
    return api.Acl(client=consul_api)


@pytest.mark.parametrize("expected", [bootstrap_response()])
async def test_bootstrap(acl, expected):
    acl.client.expected = expected
    response = await acl.bootstrap()
    assert response == bootstrap_response()


@pytest.mark.parametrize("expected", [replication_response()])
async def test_replication(acl, expected):
    acl.client.expected = expected
    response = await acl.replication()
    assert response == replication_response()


@pytest.mark.parametrize("expected", [translate_response()])
async def test_translate(acl, expected):
    acl.client.expected = expected
    response = await acl.translate(translate_payload())
    assert response == translate_response()
