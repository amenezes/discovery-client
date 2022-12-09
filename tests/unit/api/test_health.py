import pytest

from discovery import api


def sample_response():
    return [
        {
            "ID": "40e4a748-2192-161a-0510-9bf59fe950b5",
            "Node": "foobar",
            "CheckID": "serfHealth",
            "Name": "Serf Health Status",
            "Status": "passing",
            "Notes": "",
            "Output": "",
            "ServiceID": "",
            "ServiceName": "",
            "ServiceTags": [],
            "Namespace": "default",
        },
        {
            "ID": "40e4a748-2192-161a-0510-9bf59fe950b5",
            "Node": "foobar",
            "CheckID": "service:redis",
            "Name": "Service 'redis' check",
            "Status": "passing",
            "Notes": "",
            "Output": "",
            "ServiceID": "redis",
            "ServiceName": "redis",
            "ServiceTags": ["primary"],
            "Namespace": "foo",
        },
    ]


def service_response():
    return [
        {
            "Node": "foobar",
            "CheckID": "service:redis",
            "Name": "Service 'redis' check",
            "Status": "passing",
            "Notes": "",
            "Output": "",
            "ServiceID": "redis",
            "ServiceName": "redis",
            "ServiceTags": ["primary"],
            "Namespace": "default",
        }
    ]


def nodes_for_service_response():
    return [
        {
            "Node": {
                "ID": "40e4a748-2192-161a-0510-9bf59fe950b5",
                "Node": "foobar",
                "Address": "10.1.10.12",
                "Datacenter": "dc1",
                "TaggedAddresses": {"lan": "10.1.10.12", "wan": "10.1.10.12"},
                "Meta": {"instance_type": "t2.medium"},
            },
            "Service": {
                "ID": "redis",
                "Service": "redis",
                "Tags": ["primary"],
                "Address": "10.1.10.12",
                "TaggedAddresses": {
                    "lan": {"address": "10.1.10.12", "port": 8000},
                    "wan": {"address": "198.18.1.2", "port": 80},
                },
                "Meta": {"redis_version": "4.0"},
                "Port": 8000,
                "Weights": {"Passing": 10, "Warning": 1},
                "Namespace": "default",
            },
            "Checks": [
                {
                    "Node": "foobar",
                    "CheckID": "service:redis",
                    "Name": "Service 'redis' check",
                    "Status": "passing",
                    "Notes": "",
                    "Output": "",
                    "ServiceID": "redis",
                    "ServiceName": "redis",
                    "ServiceTags": ["primary"],
                    "Namespace": "default",
                },
                {
                    "Node": "foobar",
                    "CheckID": "serfHealth",
                    "Name": "Serf Health Status",
                    "Status": "passing",
                    "Notes": "",
                    "Output": "",
                    "ServiceID": "",
                    "ServiceName": "",
                    "ServiceTags": [],
                    "Namespace": "default",
                },
            ],
        }
    ]


def sample_state_response():
    return [
        {
            "Node": "foobar",
            "CheckID": "serfHealth",
            "Name": "Serf Health Status",
            "Status": "passing",
            "Notes": "",
            "Output": "",
            "ServiceID": "",
            "ServiceName": "",
            "ServiceTags": [],
            "Namespace": "default",
        },
        {
            "Node": "foobar",
            "CheckID": "service:redis",
            "Name": "Service 'redis' check",
            "Status": "passing",
            "Notes": "",
            "Output": "",
            "ServiceID": "redis",
            "ServiceName": "redis",
            "ServiceTags": ["primary"],
            "Namespace": "default",
        },
    ]


@pytest.fixture
async def health(consul_api):
    return api.Health(client=consul_api)


@pytest.mark.parametrize("expected", [sample_response()])
async def test_checks_for_node(health, expected):
    health.client.expected = expected
    response = await health.checks_for_node("my-node")
    assert response == sample_response()


@pytest.mark.parametrize("expected", [service_response()])
async def test_checks_for_service(health, expected):
    health.client.expected = expected
    response = await health.checks_for_service("my-service")
    assert response == service_response()


@pytest.mark.parametrize("expected", [nodes_for_service_response()])
async def test_service_instances(health, expected):
    health.client.expected = expected
    response = await health.service_instances("my-service")
    assert response == nodes_for_service_response()


@pytest.mark.parametrize("expected", [service_response()])
async def test_service_instances_for_connect(health, expected):
    health.client.expected = expected
    response = await health.service_instances_for_connect("consul")
    assert response == service_response()


@pytest.mark.parametrize("expected", [sample_state_response()])
async def test_checks_in_state(health, expected):
    health.client.expected = expected
    response = await health.checks_in_state()
    assert response == sample_state_response()
