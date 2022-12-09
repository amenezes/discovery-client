import pytest

from discovery import api
from discovery.api.check_status import CheckStatus

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
async def checks(consul_api):
    return api.Checks(client=consul_api)


async def test_list_checks(checks):
    checks.client.expected = CHECKS_RESPONSE
    response = await checks.list()
    assert response == CHECKS_RESPONSE


async def test_register(checks, mocker):
    spy = mocker.spy(checks.client, "put")
    await checks.register(REGISTER_PAYLOAD)
    spy.assert_called_with(
        "/v1/agent/check/register",
        json={
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
        },
    )


async def test_deregister(checks, mocker):
    spy = mocker.spy(checks.client, "put")
    await checks.deregister("my-check-id")
    spy.assert_called_with("/v1/agent/check/deregister/my-check-id")


async def test_check_pass(checks, mocker):
    spy = mocker.spy(checks.client, "put")
    await checks.check_pass("my-check-id")
    spy.assert_called_with("/v1/agent/check/pass/my-check-id")


async def test_check_warn(checks, mocker):
    spy = mocker.spy(checks.client, "put")
    await checks.check_warn("my-check-id")
    spy.assert_called_with("/v1/agent/check/warn/my-check-id")


async def test_check_fail(checks, mocker):
    spy = mocker.spy(checks.client, "put")
    await checks.check_fail("my-check-id")
    spy.assert_called_with("/v1/agent/check/fail/my-check-id")


@pytest.mark.parametrize(
    "status, expected",
    [
        ("passing", "passing"),
        (CheckStatus.WARNING, CheckStatus.WARNING),
        (CheckStatus.CRITICAL, "critical"),
    ],
)
async def test_check_update(checks, mocker, status, expected):
    spy = mocker.spy(checks.client, "put")
    await checks.check_update("my-check-id", status)
    spy.assert_called_with(
        "/v1/agent/check/update/my-check-id",
        json={"status": expected, "output": ""},
    )


@pytest.mark.parametrize("status", ["ok", "pass", "", "PASSING"])
async def test_check_update_invalid_status(checks, status):
    with pytest.raises(ValueError):
        await checks.check_update("my-check-id", status)
