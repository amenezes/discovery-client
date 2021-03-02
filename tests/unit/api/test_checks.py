import pytest

from discovery import api

CHECKS_RESPONSE = {
    "service:redis": {
        "Node": "foobar",
        "CheckID": "service:redis",
        "Name": "Service 'redis' check",
        "Status": "passing",
        "Notes": "",
        "Output": "",
        "ServiceID": "redis",
        "ServiceName": "redis",
        "ServiceTags": ["primary"],
    }
}


REGISTER_PAYLOAD = {
    "ID": "mem",
    "Name": "Memory utilization",
    "Notes": "Ensure we don't oversubscribe memory",
    "DeregisterCriticalServiceAfter": "90m",
    "Args": ["/usr/local/bin/check_mem.py"],
    "DockerContainerID": "f972c95ebf0e",
    "Shell": "/bin/bash",
    "HTTP": "https://example.com",
    "Method": "POST",
    "Header": {"Content-Type": "application/json"},
    "Body": '{"check":"mem"}',
    "TCP": "example.com:22",
    "Interval": "10s",
    "Timeout": "5s",
    "TLSSkipVerify": True,
}


@pytest.fixture
@pytest.mark.asyncio
async def checks(consul_api):
    return api.Checks(client=consul_api)


@pytest.mark.asyncio
async def test_list_checks(checks):
    checks.client.expected = CHECKS_RESPONSE
    response = await checks.checks()
    response = await response.json()
    assert response == CHECKS_RESPONSE


@pytest.mark.asyncio
async def test_register(checks):
    checks.client.expected = 200
    response = await checks.register(REGISTER_PAYLOAD)
    assert response.status == 200


@pytest.mark.asyncio
async def test_deregister(checks):
    checks.client.expected = 200
    response = await checks.deregister("my-check-id")
    assert response.status == 200


@pytest.mark.asyncio
async def test_check_pass(checks):
    checks.client.expected = 200
    response = await checks.check_pass("my-check-id")
    assert response.status == 200


@pytest.mark.asyncio
async def test_check_warn(checks):
    checks.client.expected = 200
    response = await checks.check_warn("my-check-id")
    assert response.status == 200


@pytest.mark.asyncio
async def test_check_fail(checks):
    checks.client.expected = 200
    response = await checks.check_fail("my-check-id")
    assert response.status == 200


@pytest.mark.asyncio
async def test_check_update(checks):
    checks.client.expected = 200
    response = await checks.check_update("my-check-id", "passing")
    assert response.status == 200


@pytest.mark.asyncio
async def test_check_update_value_error(checks):
    with pytest.raises(ValueError):
        await checks.check_update("my-check-id", "ok")
