import json

import pytest

from discovery import api
from tests.unit.setup import consul_api


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
@pytest.mark.asyncio
async def service(consul_api):
    return api.Service(client=consul_api)


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [list_services_response()])
async def test_services(service, expected):
    service.client.expected = expected
    response = await service.services()
    response = await response.json()
    assert response == list_services_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [service_payload_response()])
async def test_service(service, expected):
    service.client.expected = expected
    response = await service.service("web-sidecar-proxy")
    response = await response.json()
    assert response == service_payload_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_register(service, expected):
    service.client.expected = expected
    response = await service.register(register_payload())
    assert response.status == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_deregister(service, expected):
    service.client.expected = expected
    response = await service.deregister("my-service-id")
    assert response.status == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_maintenance(service, expected):
    service.client.expected = expected
    response = await service.maintenance("my-service-id", True, "For the tests")
    assert response.status == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [service_payload_response()])
async def test_configuration(service, expected):
    service.client.expected = expected
    response = await service.configuration("web-sidecar-proxy")
    response = await response.json()
    assert response == service_payload_response()
