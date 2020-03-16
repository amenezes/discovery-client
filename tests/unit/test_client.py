import pytest

import discovery
from discovery.exceptions import ServiceNotFoundException
from discovery.utils import select_one_random
from tests.unit.setup import aiohttp_client, consul_api


def service_response():
    return {
        "ID": "154d3a48-e665-a22e-c75a-c093de56a188",
        "Node": "6a4e48904f35",
        "Address": "127.0.0.1",
        "Datacenter": "dc1",
        "TaggedAddresses": {
            "lan": "127.0.0.1",
            "lan_ipv4": "127.0.0.1",
            "wan": "127.0.0.1",
            "wan_ipv4": "127.0.0.1",
        },
        "NodeMeta": {"consul-network-segment": ""},
        "ServiceKind": "",
        "ServiceID": "consul",
        "ServiceName": "consul",
        "ServiceTags": [],
        "ServiceAddress": "",
        "ServiceWeights": {"Passing": 1, "Warning": 1},
        "ServiceMeta": {
            "raft_version": "3",
            "serf_protocol_current": "2",
            "serf_protocol_max": "5",
            "serf_protocol_min": "1",
            "version": "1.7.1",
        },
        "ServicePort": 8300,
        "ServiceEnableTagOverride": False,
        "ServiceProxy": {"MeshGateway": {}, "Expose": {}},
        "ServiceConnect": {},
        "CreateIndex": 10,
        "ModifyIndex": 10,
    }


def services_response():
    return [service_response()]


def healthy_instances_response():
    return [
        {
            "Node": {
                "ID": "620b350c-5384-7797-b6be-f51696e6afc8",
                "Node": "8e195a8d9ed3",
                "Address": "127.0.0.1",
                "Datacenter": "dc1",
                "TaggedAddresses": {
                    "lan": "127.0.0.1",
                    "lan_ipv4": "127.0.0.1",
                    "wan": "127.0.0.1",
                    "wan_ipv4": "127.0.0.1",
                },
                "Meta": {"consul-network-segment": ""},
                "CreateIndex": 10,
                "ModifyIndex": 11,
            },
            "Service": {
                "ID": "consul",
                "Service": "consul",
                "Tags": [],
                "Address": "",
                "Meta": {
                    "raft_version": "3",
                    "serf_protocol_current": "2",
                    "serf_protocol_max": "5",
                    "serf_protocol_min": "1",
                    "version": "1.7.1",
                },
                "Port": 8300,
                "Weights": {"Passing": 1, "Warning": 1},
                "EnableTagOverride": False,
                "Proxy": {"MeshGateway": {}, "Expose": {}},
                "Connect": {},
                "CreateIndex": 10,
                "ModifyIndex": 10,
            },
            "Checks": [
                {
                    "Node": "8e195a8d9ed3",
                    "CheckID": "serfHealth",
                    "Name": "Serf Health Status",
                    "Status": "passing",
                    "Notes": "",
                    "Output": "Agent alive and reachable",
                    "ServiceID": "",
                    "ServiceName": "",
                    "ServiceTags": [],
                    "Type": "",
                    "Definition": {},
                    "CreateIndex": 10,
                    "ModifyIndex": 10,
                }
            ],
        }
    ]


@pytest.fixture
@pytest.mark.asyncio
async def client(consul_api):
    return discovery.Consul(client=consul_api)


@pytest.mark.asyncio
async def test_default_timeout(client):
    assert client.timeout == 30


@pytest.mark.asyncio
async def test_changing_default_timeout(aiohttp_client, monkeypatch):
    monkeypatch.setenv("DEFAULT_TIMEOUT", "5")
    client = discovery.Consul(aiohttp_client)
    assert client.timeout == 5


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [services_response()])
async def test_find_services(client, expected):
    client.client.expected = expected
    response = await client.find_services("consul")
    assert response == services_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [services_response()])
async def test_find_service_rr(client, expected):
    client.client.expected = expected
    response = await client.find_service("consul")
    assert response == service_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [services_response()])
async def test_find_service_random(client, expected):
    client.client.expected = expected
    response = await client.find_service("consul", select_one_random)
    assert response == service_response()


@pytest.mark.asyncio
async def test_service_not_found(client):
    with pytest.raises(ServiceNotFoundException):
        await client.find_service("myapp")


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", ["127.0.0.1:8300"])
async def test_leader_ip(client, expected):
    client.client.expected = expected
    leader_ip = await client.leader_ip()
    assert leader_ip == "127.0.0.1"


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [healthy_instances_response()])
async def test_consul_healthy_instances(client, expected):
    client.client.expected = expected
    response = await client.consul_healthy_instances()
    assert response == healthy_instances_response()


@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [healthy_instances_response()])
async def test_leader_current_id(client, expected):
    client.client.expected = expected
    leader_id = await client.leader_current_id()
    assert leader_id == "620b350c-5384-7797-b6be-f51696e6afc8"


@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_register(client, expected):
    client.client.expected = expected
    response = await client.register(
        "myapp", 5000, discovery.http("http://myapp:5000/status")
    )
    assert response is None


@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_deregister(client, expected):
    client.client.expected = expected
    response = await client.deregister("myapp")
    assert response is None


@pytest.mark.asyncio
async def test_deregister_fail(client):
    with pytest.raises(ServiceNotFoundException):
        await client.deregister("myapp")

    # async def test_register_additional_check(client):
    #     """Test the registration of an additional check for a service registered."""
    #     await self.dc.register_additional_check(
    #         check.Check(
    #             name='additional-check',
    #             check=check.alias('consul')
    #         )
    #     )

    # async def test_register_additional_check_failed(client):
    #     with pytest.raises(TypeError):
    #         await self.dc.register_additional_check('invalid-check')

    # async def test_deregister_additional_check(client):
    #     """Test the registration of an additional check for a service registered."""
    #     await self.dc.deregister_additional_check(
    #         check.Check(
    #             name='additional-check',
    #             check=check.alias('consul')
    #         )
    #     )

    # async def test_deregister_additional_check_failed(client):
    #     with pytest.raises(TypeError):
    #         await self.dc.deregister_additional_check('invalid-check')
