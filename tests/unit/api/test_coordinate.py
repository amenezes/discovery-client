import json

import pytest

from discovery import api


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
async def coordinate(consul_api):
    return api.Coordinate(client=consul_api)


@pytest.mark.parametrize("expected", [wan_response()])
async def test_read_wan(coordinate, expected):
    coordinate.client.expected = expected
    response = await coordinate.read_wan()
    assert response == wan_response()


@pytest.mark.parametrize("expected", [lan_response()])
async def test_read_lan_for_all_nodes(coordinate, expected):
    coordinate.client.expected = expected
    response = await coordinate.read_lan_for_all_nodes()
    assert response == lan_response()


@pytest.mark.parametrize("expected", [lan_response()])
async def test_read_lan_for_node(coordinate, expected):
    coordinate.client.expected = expected
    response = await coordinate.read_lan_for_node("agent-one")
    assert response == lan_response()


async def test_update_lan_for_node(coordinate, mocker):
    spy = mocker.spy(coordinate.client, "put")
    await coordinate.update_lan_for_node(sample_payload())
    spy.assert_called_with(
        "/v1/coordinate/update",
        json={
            "Node": "agent-one",
            "Segment": "",
            "Coord": {
                "Adjustment": 0,
                "Error": 1.5,
                "Height": 0,
                "Vec": [0, 0, 0, 0, 0, 0, 0, 0],
            },
        },
    )
