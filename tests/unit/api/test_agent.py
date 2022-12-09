import pytest

from discovery import TokenType, api


def stream_logs_sample():
    return [
        "YYYY/MM/DD HH:MM:SS [INFO] raft: Initial configuration (index=1): [{Suffrage:Voter ID:127.0.0.1:8300 Address:127.0.0.1:8300}]",
        'YYYY/MM/DD HH:MM:SS [INFO] raft: Node at 127.0.0.1:8300 [Follower] entering Follower state (Leader: "")',
        "YYYY/MM/DD HH:MM:SS [INFO] serf: EventMemberJoin: machine-osx 127.0.0.1",
        "YYYY/MM/DD HH:MM:SS [INFO] consul: Adding LAN server machine-osx (Addr: tcp/127.0.0.1:8300) (DC: dc1)",
        "YYYY/MM/DD HH:MM:SS [INFO] serf: EventMemberJoin: machine-osx.dc1 127.0.0.1",
        'YYYY/MM/DD HH:MM:SS [INFO] consul: Handled member-join event for server "machine-osx.dc1" in area "wan"',
    ]


def members_response():
    return [
        {
            "Name": "foobar",
            "Addr": "10.1.10.12",
            "Port": 8301,
            "Tags": {"bootstrap": "1", "dc": "dc1", "port": "8300", "role": "consul"},
            "Status": 1,
            "ProtocolMin": 1,
            "ProtocolMax": 2,
            "ProtocolCur": 2,
            "DelegateMin": 1,
            "DelegateMax": 3,
            "DelegateCur": 3,
        }
    ]


def configuration_response():
    return {
        "Config": {
            "Datacenter": "dc1",
            "NodeName": "foobar",
            "NodeID": "9d754d17-d864-b1d3-e758-f3fe25a9874f",
            "Server": True,
            "Revision": "deadbeef",
            "Version": "1.0.0",
        },
        "DebugConfig": {
            "... full runtime configuration ..." "... format subject to change ..."
        },
        "Coord": {"Adjustment": 0, "Error": 1.5, "Vec": [0, 0, 0, 0, 0, 0, 0, 0]},
        "Member": {
            "Name": "foobar",
            "Addr": "10.1.10.12",
            "Port": 8301,
            "Tags": {
                "bootstrap": "1",
                "dc": "dc1",
                "id": "40e4a748-2192-161a-0510-9bf59fe950b5",
                "port": "8300",
                "role": "consul",
                "vsn": "1",
                "vsn_max": "1",
                "vsn_min": "1",
            },
            "Status": 1,
            "ProtocolMin": 1,
            "ProtocolMax": 2,
            "ProtocolCur": 2,
            "DelegateMin": 2,
            "DelegateMax": 4,
            "DelegateCur": 4,
        },
        "Meta": {"instance_type": "i2.xlarge", "os_version": "ubuntu_16.04"},
    }


def metrics_response():
    return {
        "Timestamp": "2017-08-08 02:55:10 +0000 UTC",
        "Gauges": [
            {"Name": "consul.consul.session_ttl.active", "Value": 0, "Labels": {}},
            {"Name": "consul.runtime.alloc_bytes", "Value": 4704344, "Labels": {}},
            {"Name": "consul.runtime.free_count", "Value": 74063, "Labels": {}},
        ],
        "Points": [],
        "Counters": [
            {
                "Name": "consul.consul.catalog.service.query",
                "Count": 1,
                "Sum": 1,
                "Min": 1,
                "Max": 1,
                "Mean": 1,
                "Stddev": 0,
                "Labels": {"service": "consul"},
            },
            {
                "Name": "consul.raft.apply",
                "Count": 1,
                "Sum": 1,
                "Min": 1,
                "Max": 1,
                "Mean": 1,
                "Stddev": 0,
                "Labels": {},
            },
        ],
        "Samples": [
            {
                "Name": "consul.consul.http.GET.v1.agent.metrics",
                "Count": 1,
                "Sum": 0.1817069947719574,
                "Min": 0.1817069947719574,
                "Max": 0.1817069947719574,
                "Mean": 0.1817069947719574,
                "Stddev": 0,
                "Labels": {},
            },
            {
                "Name": "consul.consul.http.GET.v1.catalog.service._",
                "Count": 1,
                "Sum": 0.23342099785804749,
                "Min": 0.23342099785804749,
                "Max": 0.23342099785804749,
                "Mean": 0.23342099785804749,
                "Stddev": 0,
                "Labels": {},
            },
            {
                "Name": "consul.serf.queue.Query",
                "Count": 20,
                "Sum": 0,
                "Min": 0,
                "Max": 0,
                "Mean": 0,
                "Stddev": 0,
                "Labels": {},
            },
        ],
    }


token_payload = {"Token": "adf4238a-882b-9ddc-4a9d-5b6758e4159e"}


@pytest.fixture
async def agent(consul_api):
    return api.Agent(
        api.Checks(client=consul_api),
        api.Connect(
            api.CA(client=consul_api),
            api.Intentions(client=consul_api),
            client=consul_api,
        ),
        client=consul_api,
    )


@pytest.mark.parametrize("expected", [members_response()])
async def test_members(agent, expected):
    agent.client.expected = expected
    response = await agent.members()
    assert response == members_response()


@pytest.mark.parametrize("expected", [configuration_response()])
async def test_read_configuration(agent, expected):
    agent.client.expected = expected
    response = await agent.read_configuration()
    assert response == configuration_response()


async def test_reload(agent, mocker):
    spy = mocker.spy(agent.client, "put")
    await agent.reload()
    spy.assert_called_with("/v1/agent/reload")


async def test_maintenance(agent, mocker):
    spy = mocker.spy(agent.client, "put")
    await agent.maintenance()
    spy.assert_called_with("/v1/agent/maintenance?enable=True")


@pytest.mark.parametrize("expected", [metrics_response()])
async def test_metrics(agent, expected):
    agent.client.expected = expected
    response = await agent.metrics()
    assert response == metrics_response()


async def test_join(agent, mocker):
    spy = mocker.spy(agent.client, "put")
    await agent.join("1.2.3.4")
    spy.assert_called_with("/v1/agent/join/1.2.3.4")


async def test_leave(agent, mocker):
    spy = mocker.spy(agent.client, "put")
    await agent.leave()
    spy.assert_called_with("/v1/agent/leave")


async def test_force_leave(agent, mocker):
    spy = mocker.spy(agent.client, "put")
    await agent.force_leave("agent-one")
    spy.assert_called_with("/v1/agent/force-leave/agent-one")


@pytest.mark.parametrize(
    "token_type",
    [
        TokenType.DEFAULT,
        TokenType.AGENT,
        TokenType.AGENT_RECOVERY,
        TokenType.REPLICATION,
        TokenType.AGENT_MASTER,
        TokenType.ACL_TOKEN,
        TokenType.ACL_AGENT_TOKEN,
        TokenType.ACL_AGENT_MASTER_TOKEN,
        TokenType.ACL_REPLICATION_TOKEN,
    ],
)
async def test_update_acl_token(agent, token_type):
    await agent.update_acl_token("token", token_type)
