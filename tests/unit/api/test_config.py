import pytest

from discovery import api


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
@pytest.mark.asyncio
def config(consul_api):
    return api.Config(client=consul_api)


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_apply(config, expected):
    config.client.expected = expected
    response = await config.apply(sample_payload())
    assert response.status == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [config_response()])
async def test_get_success(config, expected):
    config.client.expected = expected
    response = await config.get("service-defaults", "web")
    response = await response.json()
    assert response == config_response()


@pytest.mark.asyncio
async def test_get_value_error(config):
    with pytest.raises(ValueError):
        await config.get("service", "web")


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [list_response()])
async def test_list_success(config, expected):
    config.client.expected = expected
    response = await config.list("service-defaults")
    response = await response.json()
    assert response == list_response()


@pytest.mark.asyncio
async def test_list_value_error(config):
    with pytest.raises(ValueError):
        await config.list("service")


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_delete_success(config, expected):
    config.client.expected = expected
    response = await config.delete("service-defaults", "web")
    assert response.status == 200


@pytest.mark.asyncio
async def test_delete_value_error(config):
    with pytest.raises(ValueError):
        await config.delete("service", "web")
