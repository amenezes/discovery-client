import json

import pytest

from discovery import api


def list_nodes_response():
    return [
        {
            "ID": "40e4a748-2192-161a-0510-9bf59fe950b5",
            "Node": "baz",
            "Address": "10.1.10.11",
            "Datacenter": "dc1",
            "TaggedAddresses": {"lan": "10.1.10.11", "wan": "10.1.10.11"},
            "Meta": {"instance_type": "t2.medium"},
        },
        {
            "ID": "8f246b77-f3e1-ff88-5b48-8ec93abf3e05",
            "Node": "foobar",
            "Address": "10.1.10.12",
            "Datacenter": "dc2",
            "TaggedAddresses": {"lan": "10.1.10.11", "wan": "10.1.10.12"},
            "Meta": {"instance_type": "t2.large"},
        },
    ]


def list_datacenters_response():
    return json.dumps(["dc1", "dc2"])


def map_services_node_response():
    return {
        "Node": {
            "ID": "40e4a748-2192-161a-0510-9bf59fe950b5",
            "Node": "foobar",
            "Address": "10.1.10.12",
            "Datacenter": "dc1",
            "TaggedAddresses": {"lan": "10.1.10.12", "wan": "10.1.10.12"},
            "Meta": {"instance_type": "t2.medium"},
        },
        "Services": {
            "consul": {
                "ID": "consul",
                "Service": "consul",
                "Tags": None,
                "Meta": {},
                "Port": 8300,
            },
            "redis": {
                "ID": "redis",
                "Service": "redis",
                "TaggedAddresses": {
                    "lan": {"address": "10.1.10.12", "port": 8000},
                    "wan": {"address": "198.18.1.2", "port": 80},
                },
                "Tags": ["v1"],
                "Meta": {"redis_version": "4.0"},
                "Port": 8000,
                "Namespace": "default",
            },
        },
    }


def service_response():
    return [
        {
            "ID": "40e4a748-2192-161a-0510-9bf59fe950b5",
            "Node": "foobar",
            "Address": "192.168.10.10",
            "Datacenter": "dc1",
            "TaggedAddresses": {"lan": "192.168.10.10", "wan": "10.0.10.10"},
            "NodeMeta": {"somekey": "somevalue"},
            "CreateIndex": 51,
            "ModifyIndex": 51,
            "ServiceAddress": "172.17.0.3",
            "ServiceEnableTagOverride": False,
            "ServiceID": "32a2a47f7992:nodea:5000",
            "ServiceName": "foobar",
            "ServicePort": 5000,
            "ServiceMeta": {"foobar_meta_value": "baz"},
            "ServiceTaggedAddresses": {
                "lan": {"address": "172.17.0.3", "port": 5000},
                "wan": {"address": "198.18.0.1", "port": 512},
            },
            "ServiceTags": ["tacos"],
            "ServiceProxy": {
                "DestinationServiceName": "",
                "DestinationServiceID": "",
                "LocalServiceAddress": "",
                "LocalServicePort": 0,
                "Config": None,
                "Upstreams": None,
            },
            "ServiceConnect": {"Native": False, "Proxy": None},
            "Namespace": "default",
        }
    ]


def services_response():
    return {"consul": [], "redis": [], "postgresql": ["primary", "secondary"]}


@pytest.fixture
async def catalog(consul_api):
    return api.Catalog(client=consul_api)


async def test_register_entity(catalog, mocker):
    spy = mocker.spy(catalog.client, "put")
    await catalog.register_entity(
        "192.168.10.10", "dc1", "t2.320", "40e4a748-2192-161a-0510-9bf59fe950b5"
    )
    spy.assert_called_with(
        "/v1/catalog/register",
        json={
            "Datacenter": "dc1",
            "ID": "40e4a748-2192-161a-0510-9bf59fe950b5",
            "Node": "t2.320",
            "Address": "192.168.10.10",
        },
    )


async def test_deregister_entity(catalog, mocker):
    spy = mocker.spy(catalog.client, "put")
    await catalog.deregister_entity("t2.320", "dc1")
    spy.assert_called_with(
        "/v1/catalog/deregister", json={"Datacenter": "dc1", "Node": "t2.320"}
    )


@pytest.mark.parametrize("expected", [list_datacenters_response()])
async def test_datacenters(catalog, expected):
    catalog.client.expected = expected
    response = await catalog.list_datacenters()
    assert response == list_datacenters_response()


@pytest.mark.parametrize("expected", [list_nodes_response()])
async def test_list_nodes(catalog, expected):
    catalog.client.expected = expected
    response = await catalog.list_nodes()
    assert response == list_nodes_response()


@pytest.mark.parametrize("expected", [services_response()])
async def test_list_services(catalog, expected):
    catalog.client.expected = expected
    response = await catalog.list_services()
    assert response == services_response()


@pytest.mark.parametrize("expected", [service_response()])
async def test_list_nodes_for_service(catalog, expected):
    catalog.client.expected = expected
    response = await catalog.list_nodes_for_service("my-service")
    assert response == service_response()


@pytest.mark.parametrize("expected", [service_response()])
async def test_list_nodes_for_connect(catalog, expected):
    catalog.client.expected = expected
    response = await catalog.list_nodes_for_connect("my-service")
    assert response == service_response()


@pytest.mark.parametrize("expected", [map_services_node_response()])
async def test_services_for_node(catalog, expected):
    catalog.client.expected = expected
    response = await catalog.services_for_node("my-node")
    assert response == map_services_node_response()
