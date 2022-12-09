import pytest

from discovery import api


def list_services_response():
    return {
        "redis": {
            "ID": "redis",
            "Service": "redis",
            "Tags": [],
            "TaggedAddresses": {
                "lan": {"address": "127.0.0.1", "port": 8000},
                "wan": {"address": "198.18.0.53", "port": 80},
            },
            "Meta": {"redis_version": "4.0"},
            "Port": 8000,
            "Address": "",
            "EnableTagOverride": False,
            "Weights": {"Passing": 10, "Warning": 1},
        }
    }


def register_payload():
    return {
        "ID": "redis1",
        "Name": "redis",
        "Tags": ["primary", "v1"],
        "Address": "127.0.0.1",
        "Port": 8000,
        "Meta": {"redis_version": "4.0"},
        "EnableTagOverride": False,
        "Check": {
            "DeregisterCriticalServiceAfter": "90m",
            "Args": ["/usr/local/bin/check_redis.py"],
            "Interval": "10s",
            "Timeout": "5s",
        },
        "Weights": {"Passing": 10, "Warning": 1},
    }


def service_health_id_response():
    return {
        "passing": {
            "ID": "web1",
            "Service": "web",
            "Tags": ["rails"],
            "Address": "",
            "TaggedAddresses": {
                "lan": {"address": "127.0.0.1", "port": 8000},
                "wan": {"address": "198.18.0.53", "port": 80},
            },
            "Meta": None,
            "Port": 80,
            "EnableTagOverride": False,
            "Connect": {"Native": False, "Proxy": None},
            "CreateIndex": 0,
            "ModifyIndex": 0,
        }
    }


def service_health_name_response():
    return {
        "critical": [
            {
                "ID": "web2",
                "Service": "web",
                "Tags": ["rails"],
                "Address": "",
                "TaggedAddresses": {
                    "lan": {"address": "127.0.0.1", "port": 8000},
                    "wan": {"address": "198.18.0.53", "port": 80},
                },
                "Meta": None,
                "Port": 80,
                "EnableTagOverride": False,
                "Connect": {"Native": False, "Proxy": None},
                "CreateIndex": 0,
                "ModifyIndex": 0,
            }
        ],
        "passing": [
            {
                "ID": "web1",
                "Service": "web",
                "Tags": ["rails"],
                "Address": "",
                "TaggedAddresses": {
                    "lan": {"address": "127.0.0.1", "port": 8000},
                    "wan": {"address": "198.18.0.53", "port": 80},
                },
                "Meta": None,
                "Port": 80,
                "EnableTagOverride": False,
                "Connect": {"Native": False, "Proxy": None},
                "CreateIndex": 0,
                "ModifyIndex": 0,
            }
        ],
    }


def service_payload_response():
    return {
        "Kind": "connect-proxy",
        "ID": "web-sidecar-proxy",
        "Service": "web-sidecar-proxy",
        "Tags": None,
        "Meta": None,
        "Port": 18080,
        "Address": "",
        "TaggedAddresses": {
            "lan": {"address": "127.0.0.1", "port": 8000},
            "wan": {"address": "198.18.0.53", "port": 80},
        },
        "Weights": {"Passing": 1, "Warning": 1},
        "EnableTagOverride": False,
        "ContentHash": "4ecd29c7bc647ca8",
        "Proxy": {
            "DestinationServiceName": "web",
            "DestinationServiceID": "web",
            "LocalServiceAddress": "127.0.0.1",
            "LocalServicePort": 8080,
            "Config": {"foo": "bar"},
            "Upstreams": [
                {
                    "DestinationType": "service",
                    "DestinationName": "db",
                    "LocalBindPort": 9191,
                }
            ],
        },
    }


def status_response():
    return {
        "passing": {
            "ID": "web1",
            "Service": "web",
            "Tags": ["rails"],
            "Address": "",
            "TaggedAddresses": {
                "lan": {"address": "127.0.0.1", "port": 8000},
                "wan": {"address": "198.18.0.53", "port": 80},
            },
            "Meta": None,
            "Port": 80,
            "EnableTagOverride": False,
            "Connect": {"Native": False, "Proxy": None},
            "CreateIndex": 0,
            "ModifyIndex": 0,
        }
    }


@pytest.fixture
async def service(consul_api):
    return api.Service(client=consul_api)


@pytest.mark.parametrize("expected", [list_services_response()])
async def test_list(service, expected):
    service.client.expected = expected
    response = await service.list()
    assert response == list_services_response()


async def test_register(service, mocker):
    spy = mocker.spy(service.client, "put")
    await service.register(register_payload())
    spy.assert_called_with(
        "/v1/agent/service/register",
        json={
            "ID": "redis1",
            "Name": "redis",
            "Tags": ["primary", "v1"],
            "Address": "127.0.0.1",
            "Port": 8000,
            "Meta": {"redis_version": "4.0"},
            "EnableTagOverride": False,
            "Check": {
                "DeregisterCriticalServiceAfter": "90m",
                "Args": ["/usr/local/bin/check_redis.py"],
                "Interval": "10s",
                "Timeout": "5s",
            },
            "Weights": {"Passing": 10, "Warning": 1},
        },
    )


async def test_deregister(service, mocker):
    spy = mocker.spy(service.client, "put")
    await service.deregister("my-service-id")
    spy.assert_called_with(
        "/v1/agent/service/deregister/my-service-id",
    )


@pytest.mark.parametrize(
    "reason, expected",
    [
        (None, "/v1/agent/service/maintenance/my-service-id?enable=True"),
        (
            "For the tests",
            "/v1/agent/service/maintenance/my-service-id?enable=True&reason=For+the+tests",
        ),
    ],
)
async def test_enable_maintenance(reason, expected, service, mocker):
    spy = mocker.spy(service.client, "put")
    await service.enable_maintenance("my-service-id", True, reason)
    spy.assert_called_with(expected)


@pytest.mark.parametrize("expected", [service_payload_response()])
async def test_configuration(service, expected):
    service.client.expected = expected
    response = await service.configuration("web-sidecar-proxy")
    assert response == service_payload_response()


@pytest.mark.parametrize("expected", [service_health_name_response()])
async def test_health_by_name(service, expected):
    service.client.expected = expected
    response = await service.health_by_name("web")
    assert response == service_health_name_response()


@pytest.mark.parametrize("expected", [service_health_id_response()])
async def test_health_by_id(service, expected):
    service.client.expected = expected
    response = await service.health_by_id("web1")
    assert response == service_health_id_response()
