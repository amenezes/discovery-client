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

READ_AUTOPILOT_STATE_RESP = {
    "Healthy": True,
    "FailureTolerance": 1,
    "OptimisticFailureTolerance": 4,
    "Servers": {
        "5e26a3af-f4fc-4104-a8bb-4da9f19cb278": {},
        "10b71f14-4b08-4ae5-840c-f86d39e7d330": {},
        "1fd52e5e-2f72-47d3-8cfc-2af760a0c8c2": {},
        "63783741-abd7-48a9-895a-33d01bf7cb30": {},
        "6cf04fd0-7582-474f-b408-a830b5471285": {},
    },
    "Leader": "5e26a3af-f4fc-4104-a8bb-4da9f19cb278",
    "Voters": [
        "5e26a3af-f4fc-4104-a8bb-4da9f19cb278",
        "10b71f14-4b08-4ae5-840c-f86d39e7d330",
        "1fd52e5e-2f72-47d3-8cfc-2af760a0c8c2",
    ],
    "RedundancyZones": {"az1": {}, "az2": {}, "az3": {}},
    "ReadReplicas": [
        "63783741-abd7-48a9-895a-33d01bf7cb30",
        "6cf04fd0-7582-474f-b408-a830b5471285",
    ],
    "Upgrade": {},
}


async def test_read_configuration(autopilot):
    autopilot.client.expected = CONFIG_RESPONSE
    response = await autopilot.read_configuration()
    assert response == CONFIG_RESPONSE


async def test_update_configuration(autopilot, mocker):
    spy = mocker.spy(autopilot.client, "put")
    await autopilot.update_configuration(SAMPLE_PAYLOAD)
    spy.assert_called_with(
        "/v1/operator/autopilot/configuration",
        json={
            "CleanupDeadServers": {
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
            },
            "LastContactThreshold": "200ms",
            "MaxTrailingLogs": 250,
            "MinQuorum": 0,
            "ServerStabilizationTime": "10s",
            "RedundancyZoneTag": "",
            "DisableUpgradeMigration": False,
            "UpgradeVersionTag": "",
        },
    )


async def test_read_health(autopilot):
    autopilot.client.expected = HEALTH_RESPONSE
    response = await autopilot.read_health()
    assert response == HEALTH_RESPONSE


async def test_read_state(autopilot):
    autopilot.client.expected = READ_AUTOPILOT_STATE_RESP
    response = await autopilot.read_state()
    assert response == READ_AUTOPILOT_STATE_RESP
