import json

import pytest


def create_area_response():
    return {"ID": "8f246b77-f3e1-ff88-5b48-8ec93abf3e05"}


def area_payload():
    return json.dumps(
        [
            {
                "ID": "8f246b77-f3e1-ff88-5b48-8ec93abf3e05",
                "PeerDatacenter": "dc2",
                "RetryJoin": ["10.1.2.3", "10.1.2.4", "10.1.2.5"],
            }
        ]
    )


def list_area_response():
    return [
        {
            "ID": "8f246b77-f3e1-ff88-5b48-8ec93abf3e05",
            "PeerDatacenter": "dc2",
            "RetryJoin": ["10.1.2.3", "10.1.2.4", "10.1.2.5"],
        }
    ]


def join_payload():
    return ["10.1.2.3", "10.1.2.4", "10.1.2.5"]


def join_response():
    return json.dumps(
        [
            {"Address": "10.1.2.3", "Joined": True, "Error": ""},
            {"Address": "10.1.2.4", "Joined": True, "Error": ""},
            {"Address": "10.1.2.5", "Joined": True, "Error": ""},
        ]
    )


def members_response():
    return json.dumps(
        [
            {
                "ID": "afc5d95c-1eee-4b46-b85b-0efe4c76dd48",
                "Name": "node-2.dc1",
                "Addr": "127.0.0.2",
                "Port": 8300,
                "Datacenter": "dc1",
                "Role": "server",
                "Build": "0.8.0",
                "Protocol": 2,
                "Status": "alive",
                "RTT": 256478,
            },
        ]
    )


@pytest.mark.parametrize("expected", [create_area_response()])
async def test_create_network(area, expected):
    area.client.expected = expected
    response = await area.create_network("dc2")
    assert response == create_area_response()


@pytest.mark.parametrize("expected", [list_area_response()])
async def test_list_network(area, expected):
    area.client.expected = expected
    response = await area.list_network()
    assert response == list_area_response()


@pytest.mark.parametrize("expected", [list_area_response()])
async def test_list_specific_network(area, expected):
    area.client.expected = expected
    response = await area.list_specific_network("8f246b77-f3e1-ff88-5b48-8ec93abf3e05")
    assert response == list_area_response()


async def test_update_network(area, mocker):
    spy = mocker.spy(area.client, "put")
    await area.update_network("8f246b77-f3e1-ff88-5b48-8ec93abf3e05")
    spy.assert_called_with(
        "/v1/operator/area/8f246b77-f3e1-ff88-5b48-8ec93abf3e05", json={"UseTLS": True}
    )


async def test_delete_network(area, mocker):
    spy = mocker.spy(area.client, "delete")
    await area.delete_network("8f246b77-f3e1-ff88-5b48-8ec93abf3e05")
    spy.assert_called_with("/v1/operator/area/8f246b77-f3e1-ff88-5b48-8ec93abf3e05")


@pytest.mark.parametrize("expected", [join_response()])
async def test_join_network(area, expected):
    area.client.expected = expected
    response = await area.join_network(
        "8f246b77-f3e1-ff88-5b48-8ec93abf3e05",
        join_payload(),
    )
    assert response == join_response()


@pytest.mark.parametrize("expected", [members_response()])
async def test_list_network_members(area, expected):
    area.client.expected = expected
    response = await area.list_network_members("8f246b77-f3e1-ff88-5b48-8ec93abf3e05")
    assert response == members_response()
