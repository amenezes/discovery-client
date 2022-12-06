import pytest

from discovery import api
from discovery.api.kind import Kind


def sample_payload():
    return {
        "Kind": "service-defaults",
        "Name": "web",
        "Protocol": "http",
    }


def config_response():
    return {
        "Kind": "service-defaults",
        "Name": "web",
        "Protocol": "http",
        "CreateIndex": 15,
        "ModifyIndex": 35,
    }


def list_response():
    return [
        {
            "Kind": "service-defaults",
            "Name": "db",
            "Protocol": "tcp",
            "CreateIndex": 16,
            "ModifyIndex": 16,
        },
        {
            "Kind": "service-defaults",
            "Name": "web",
            "Protocol": "http",
            "CreateIndex": 13,
            "ModifyIndex": 13,
        },
    ]


@pytest.fixture
def config(consul_api):
    return api.Config(client=consul_api)


async def test_apply(config, mocker):
    spy = mocker.spy(config.client, "put")
    await config.apply(sample_payload())
    spy.assert_called_with(
        "/v1/config",
        json={"Kind": "service-defaults", "Name": "web", "Protocol": "http"},
    )


@pytest.mark.parametrize("expected", [config_response()])
async def test_get(config, expected):
    config.client.expected = expected
    response = await config.get(Kind.SERVICE_DEFAULTS, "web")
    assert response == config_response()


@pytest.mark.parametrize("expected", [list_response()])
async def test_list(config, expected):
    config.client.expected = expected
    response = await config.list(Kind.SERVICE_DEFAULTS)
    assert response == list_response()


async def test_delete(config, mocker):
    spy = mocker.spy(config.client, "delete")
    await config.delete(Kind.SERVICE_DEFAULTS, "web")
    spy.assert_called_with("/v1/config/service-defaults/web")
