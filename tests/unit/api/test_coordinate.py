import json

import pytest

from discovery import api
from tests.unit.setup import consul_api


def sample_payload():
    return {
        "Node": "agent-one",
        "Segment": "",
        "Coord": {
            "Adjustment": 0,
            "Error": 1.5,
            "Height": 0,
            "Vec": [0, 0, 0, 0, 0, 0, 0, 0],
        },
    }


def wan_response():
    return json.dumps(
        {
            "Node": "agent-one",
            "Segment": "",
            "Coord": {
                "Adjustment": 0,
                "Error": 1.5,
                "Height": 0,
                "Vec": [0, 0, 0, 0, 0, 0, 0, 0],
            },
        }
    )


def lan_response():
    return [wan_response()]


@pytest.fixture
@pytest.mark.asyncio
async def coordinate(consul_api):
    return api.Coordinate(client=consul_api)


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [wan_response()])
async def test_read_wan(coordinate, expected):
    coordinate.client.expected = expected
    response = await coordinate.read_wan()
    response = await response.json()
    assert response == wan_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [lan_response()])
async def test_read_lan(coordinate, expected):
    coordinate.client.expected = expected
    response = await coordinate.read_lan()
    response = await response.json()
    assert response == lan_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [lan_response()])
async def test_read_lan_node(coordinate, expected):
    coordinate.client.expected = expected
    response = await coordinate.read_lan_node("agent-one")
    response = await response.json()
    assert response == lan_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_update_lan_node(coordinate, expected):
    coordinate.client.expected = expected
    response = await coordinate.update_lan_node(sample_payload())
    assert response.status == 200
