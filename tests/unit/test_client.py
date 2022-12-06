SERVICE_RESPONSE = {
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


SERVICES_RESPONSE = [SERVICE_RESPONSE]


HEALTHY_INSTANCES_RESPONSE = [
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


async def test_default_timeout(consul):
    assert consul.timeout == 30
