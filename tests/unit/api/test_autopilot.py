import pytest

SAMPLE_PAYLOAD = {
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

CONFIG_RESPONSE = {
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


HEALTH_RESPONSE = {
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
async def test_read_configuration(autopilot):
    autopilot.client.expected = CONFIG_RESPONSE
    response = await autopilot.read_configuration()
    response = await response.json()
    assert response == CONFIG_RESPONSE


@pytest.mark.asyncio
async def test_update_configuration(autopilot):
    autopilot.client.expected = 200
    response = await autopilot.update_configuration(SAMPLE_PAYLOAD)
    assert response.status == 200


@pytest.mark.asyncio
async def test_read_health(autopilot):
    autopilot.client.expected = HEALTH_RESPONSE
    response = await autopilot.read_health()
    response = await response.json()
    assert response == HEALTH_RESPONSE
