import json

import pytest

from discovery import api


def sample_payload():
    return json.dumps(
        [
            {
                "KV": {
                    "Verb": "get",
                    "Key": "<key>",
                    "Value": "<Base64-encoded blob of data>",
                    "Flags": "<flags>",
                    "Index": "<index>",
                    "Session": "<session id>",
                }
            },
            {
                "Node": {
                    "Verb": "set",
                    "Node": {
                        "ID": "67539c9d-b948-ba67-edd4-d07a676d6673",
                        "Node": "bar",
                        "Address": "192.168.0.1",
                        "Datacenter": "dc1",
                        "Meta": {"instance_type": "m2.large"},
                    },
                }
            },
            {"Service": {"Verb": "delete", "Node": "foo", "Service": {"ID": "db1"}}},
            {
                "Check": {
                    "Verb": "cas",
                    "Check": {
                        "Node": "bar",
                        "CheckID": "service:web1",
                        "Name": "Web HTTP Check",
                        "Status": "critical",
                        "ServiceID": "web1",
                        "ServiceName": "web",
                        "ServiceTags": None,
                        "Definition": {
                            "HTTP": "http://localhost:8080",
                            "Interval": "10s",
                        },
                        "ModifyIndex": 22,
                    },
                }
            },
        ]
    )


@pytest.fixture
@pytest.mark.asyncio
async def txn(consul_api):
    return api.Txn(client=consul_api)


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_create(txn, expected):
    txn.client.expected = expected
    response = await txn.create(sample_payload())
    assert response.status == 200
