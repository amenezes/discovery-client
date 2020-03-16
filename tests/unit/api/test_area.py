import json

import pytest

from discovery import api
from tests.unit.setup import consul_api


def sample_payload():
    return json.dumps(
        {
            "PeerDatacenter": "dc2",
            "RetryJoin": ["10.1.2.3", "10.1.2.4", "10.1.2.5"],
            "UseTLS": False,
        }
    )


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


def update_area_payload():
    return {"UseTLS": True}


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


@pytest.fixture
@pytest.mark.asyncio
def area(consul_api):
    return api.Area(client=consul_api)


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [create_area_response()])
async def test_create(area, expected):
    area.client.expected = expected
    response = await area.create(sample_payload())
    response = await response.json()
    assert response == create_area_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [list_area_response()])
async def test_list_areas(area, expected):
    area.client.expected = expected
    response = await area.list()
    response = await response.json()
    assert response == list_area_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [list_area_response()])
async def test_list_specific_area(area, expected):
    area.client.expected = expected
    response = await area.list("8f246b77-f3e1-ff88-5b48-8ec93abf3e05")
    response = await response.json()
    assert response == list_area_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_update(area, expected):
    area.client.expected = expected
    response = await area.update(
        "8f246b77-f3e1-ff88-5b48-8ec93abf3e05", update_area_payload()
    )
    assert response.status == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_delete(area, expected):
    area.client.expected = expected
    response = await area.delete("8f246b77-f3e1-ff88-5b48-8ec93abf3e05")
    assert response.status == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [join_response()])
async def test_join(area, expected):
    area.client.expected = expected
    response = await area.join("8f246b77-f3e1-ff88-5b48-8ec93abf3e05", join_payload(),)
    response = await response.json()
    assert response == join_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [members_response()])
async def test_members(area, expected):
    area.client.expected = expected
    response = await area.members("8f246b77-f3e1-ff88-5b48-8ec93abf3e05")
    response = await response.json()
    assert response == members_response()
