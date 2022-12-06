import pytest

from discovery import api


def sample_response():
    return {"ID": "8f246b77-f3e1-ff88-5b48-8ec93abf3e05"}


def sample_read_response():
    return [
        {
            "ID": "8f246b77-f3e1-ff88-5b48-8ec93abf3e05",
            "Name": "my-query",
            "Session": "adf4238a-882b-9ddc-4a9d-5b6758e4159e",
            "Token": "<hidden>",
            "Service": {
                "Service": "redis",
                "Failover": {"NearestN": 3, "Datacenters": ["dc1", "dc2"]},
                "OnlyPassing": False,
                "Tags": ["primary", "!experimental"],
                "NodeMeta": {"instance_type": "m3.large"},
                "ServiceMeta": {"environment": "production"},
            },
            "DNS": {"TTL": "10s"},
            "RaftIndex": {"CreateIndex": 23, "ModifyIndex": 42},
        }
    ]


def sample_execute_response():
    return {
        "Service": "redis",
        "Nodes": [
            {
                "Node": {
                    "ID": "40e4a748-2192-161a-0510-9bf59fe950b5",
                    "Node": "foobar",
                    "Address": "10.1.10.12",
                    "Datacenter": "dc1",
                    "TaggedAddresses": {"lan": "10.1.10.12", "wan": "10.1.10.12"},
                    "NodeMeta": {"instance_type": "m3.large"},
                },
                "Service": {
                    "ID": "redis",
                    "Service": "redis",
                    "Tags": None,
                    "Meta": {"redis_version": "4.0"},
                    "Port": 8000,
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
                    },
                ],
                "DNS": {"TTL": "10s"},
                "Datacenter": "dc3",
                "Failovers": 2,
            }
        ],
    }


def sample_explain_response():
    return {
        "Query": {
            "ID": "8f246b77-f3e1-ff88-5b48-8ec93abf3e05",
            "Name": "my-query",
            "Session": "adf4238a-882b-9ddc-4a9d-5b6758e4159e",
            "Token": "<hidden>",
            # 'Name': 'geo-db',
            "Template": {
                "Type": "name_prefix_match",
                "Regexp": "^geo-db-(.*?)-([^\\-]+?)$",
            },
            "Service": {
                "Service": "mysql-customer",
                "Failover": {"NearestN": 3, "Datacenters": ["dc1", "dc2"]},
                "OnlyPassing": True,
                "Tags": ["primary"],
                "Meta": {"mysql_version": "5.7.20"},
                "NodeMeta": {"instance_type": "m3.large"},
            },
        }
    }


@pytest.fixture
def query(consul_api):
    return api.Query(client=consul_api)


@pytest.mark.parametrize("expected", [sample_response()])
async def test_create(query, expected):
    query.client.expected = expected
    response = await query.create(
        "my-query",
        {
            "Service": "redis",
            "Failover": {"NearestN": 3, "Datacenters": ["dc1", "dc2"]},
            "Near": "node1",
            "OnlyPassing": False,
            "Tags": ["primary", "!experimental"],
            "NodeMeta": {"instance_type": "m3.large"},
            "ServiceMeta": {"environment": "production"},
        },
        session="adf4238a-882b-9ddc-4a9d-5b6758e4159e",
        dns={"TTL": "10s"},
    )
    assert response == sample_response()


@pytest.mark.parametrize("expected", [sample_read_response()])
async def test_read(query, expected):
    query.client.expected = expected
    response = await query.read("8f246b77-f3e1-ff88-5b48-8ec93abf3e05")
    assert response == sample_read_response()


async def test_delete(query, mocker):
    spy = mocker.spy(query.client, "delete")
    await query.delete("8f246b77-f3e1-ff88-5b48-8ec93abf3e05")
    spy.assert_called_with("/v1/query/8f246b77-f3e1-ff88-5b48-8ec93abf3e05")


async def test_update(query):
    await query.update(
        "8f246b77-f3e1-ff88-5b48-8ec93abf3e05",
        name="my-query",
        session="adf4238a-882b-9ddc-4a9d-5b6758e4159e",
        token="",
        service={
            "Service": "redis",
            "Failover": {"NearestN": 3, "Datacenters": ["dc1", "dc2"]},
            "Near": "node1",
            "OnlyPassing": False,
            "Tags": ["primary", "!experimental"],
            "NodeMeta": {"instance_type": "m3.large"},
            "ServiceMeta": {"environment": "production"},
        },
        dns={"TTL": "10s"},
    )


@pytest.mark.parametrize("expected", [sample_execute_response()])
async def test_execute(query, expected):
    query.client.expected = expected
    response = await query.execute("8f246b77-f3e1-ff88-5b48-8ec93abf3e05")
    assert response == sample_execute_response()


@pytest.mark.parametrize("expected", [sample_explain_response()])
async def test_explain(query, expected):
    query.client.expected = expected
    response = await query.explain("8f246b77-f3e1-ff88-5b48-8ec93abf3e05")
    assert response == sample_explain_response()
