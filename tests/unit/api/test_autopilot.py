import json

import pytest


def sample_payload():
    return json.dumps(
        {
            "CleanupDeadServers": True,
            "LastContactThreshold": "100ms",
            "MaxTrailingLogs": 250,
            "MinQuorum": 3,
            "ServerStabilizationTime": "5s",
            "RedundancyZoneTag": "",
            "DisableUpgradeMigration": False,
            "UpgradeVersionTag": "",
            "CreateIndex": 4,
            "ModifyIndex": 4,
        }
    )


def config_response():
    return {
        "CleanupDeadServers": True,
        "LastContactThreshold": "200ms",
        "MaxTrailingLogs": 250,
        "ServerStabilizationTime": "10s",
        "RedundancyZoneTag": "",
        "DisableUpgradeMigration": False,
        "UpgradeVersionTag": "",
        "CreateIndex": 4,
        "ModifyIndex": 4,
    }


def health_response():
    return {
        "Healthy": True,
        "FailureTolerance": 0,
        "Servers": [
            {
                "ID": "e349749b-3303-3ddf-959c-b5885a0e1f6e",
                "Name": "node1",
                "Address": "127.0.0.1:8300",
                "SerfStatus": "alive",
                "Version": "0.7.4",
                "Leader": True,
                "LastContact": "0s",
                "LastTerm": 2,
                "LastIndex": 46,
                "Healthy": True,
                "Voter": True,
                "StableSince": "2017-03-06T22:07:51Z",
            },
            {
                "ID": "e36ee410-cc3c-0a0c-c724-63817ab30303",
                "Name": "node2",
                "Address": "127.0.0.1:8205",
                "SerfStatus": "alive",
                "Version": "0.7.4",
                "Leader": False,
                "LastContact": "27.291304ms",
                "LastTerm": 2,
                "LastIndex": 46,
                "Healthy": True,
                "Voter": False,
                "StableSince": "2017-03-06T22:18:26Z",
            },
        ],
    }


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [config_response()])
async def test_read_configuration(autopilot, expected):
    autopilot.client.expected = expected
    response = await autopilot.read_configuration()
    response = await response.json()
    assert response == config_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_update_configuration(autopilot, expected):
    autopilot.client.expected = expected
    response = await autopilot.update_configuration(sample_payload)
    assert response.status == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [health_response()])
async def test_read_health(autopilot, expected):
    autopilot.client.expected = expected
    response = await autopilot.read_health()
    response = await response.json()
    assert response == health_response()
