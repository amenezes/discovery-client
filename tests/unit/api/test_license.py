import json

import pytest


def sample_payload(*args, **kwargs):
    return json.dumps(
        {
            "Valid": True,
            "License": {
                "license_id": "2afbf681-0d1a-0649-cb6c-333ec9f0989c",
                "customer_id": "0259271d-8ffc-e85e-0830-c0822c1f5f2b",
                "installation_id": "*",
                "issue_time": "2018-05-21T20:03:35.911567355Z",
                "start_time": "2018-05-21T04:00:00Z",
                "expiration_time": "2019-05-22T03:59:59.999Z",
                "product": "consul",
                "flags": {"package": "premium"},
                "features": [
                    "Automated Backups",
                    "Automated Upgrades",
                    "Enhanced Read Scalability",
                    "Network Segments",
                    "Redundancy Zone",
                    "Advanced Network Federation",
                ],
                "temporary": False,
            },
            "Warnings": [],
        }
    )


@pytest.mark.parametrize("expected", [sample_payload()])
async def test_current(license, expected):
    license.client.expected = expected
    response = await license.current()
    assert response == sample_payload()


@pytest.mark.parametrize("expected", [sample_payload()])
async def test_update(license, expected):
    license.client.expected = expected
    response = await license.update(data={})
    assert response == sample_payload()


@pytest.mark.parametrize("expected", [sample_payload()])
async def test_reset(license, expected):
    license.client.expected = expected
    response = await license.reset()
    assert response == sample_payload()
