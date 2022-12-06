import pytest

from discovery import api


def sample_payload():
    return "Lorem ipsum dolor sit amet, consectetur adipisicing elit..."


def sample_response():
    return {
        "ID": "b54fe110-7af5-cafc-d1fb-afc8ba432b1c",
        "Name": "deploy",
        "Payload": None,
        "NodeFilter": "",
        "ServiceFilter": "",
        "TagFilter": "",
        "Version": 1,
        "LTime": 0,
    }


def list_response():
    return [sample_response()]


@pytest.fixture
async def events(consul_api):
    return api.Events(client=consul_api)


@pytest.mark.parametrize("expected", [sample_response()])
async def test_fire(events, expected):
    events.client.expected = expected
    response = await events.fire_event("my-event", sample_payload())
    assert response == sample_response()


@pytest.mark.parametrize("expected", [list_response()])
async def test_list(events, expected):
    events.client.expected = expected
    response = await events.list()
    assert response == list_response()
