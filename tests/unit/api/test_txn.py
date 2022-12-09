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


SAMPLE_RESPONSE = {
    "Results": [
        {
            "KV": {
                "LockIndex": "<lock index>",
                "Key": "<key>",
                "Flags": "<flags>",
                "Value": "<Base64-encoded blob of data, or null>",
                "CreateIndex": "<index>",
                "ModifyIndex": "<index>",
            }
        },
        {
            "Node": {
                "ID": "67539c9d-b948-ba67-edd4-d07a676d6673",
                "Node": "bar",
                "Address": "192.168.0.1",
                "Datacenter": "dc1",
                "TaggedAddresses": None,
                "Meta": {"instance_type": "m2.large"},
                "CreateIndex": 32,
                "ModifyIndex": 32,
            }
        },
        {
            "Check": {
                "Node": "bar",
                "CheckID": "service:web1",
                "Name": "Web HTTP Check",
                "Status": "critical",
                "Notes": "",
                "Output": "",
                "ServiceID": "web1",
                "ServiceName": "web",
                "ServiceTags": None,
                "Definition": {"HTTP": "http://localhost:8080", "Interval": "10s"},
                "CreateIndex": 22,
                "ModifyIndex": 35,
            }
        },
    ],
    "Errors": [
        {
            "OpIndex": "<index of failed operation>",
            "What": "<error message for failed operation>",
        },
        ...,
    ],
}


@pytest.fixture
async def txn(consul_api):
    return api.Txn(client=consul_api)


async def test_create(txn):
    txn.client.expected = SAMPLE_RESPONSE
    response = await txn.create(sample_payload())
    assert response == SAMPLE_RESPONSE
