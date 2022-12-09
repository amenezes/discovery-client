import pytest

from discovery import api


@pytest.fixture
async def operator(consul_api, area, autopilot, keyring, license, raft, segment):
    return api.Operator(
        area,
        autopilot,
        keyring,
        license,
        raft,
        segment,
        client=consul_api,
    )


async def test_area(operator, area):
    assert operator.area == area


async def test_autopilot(operator, autopilot):
    assert operator.autopilot == autopilot


async def test_keyring(operator, keyring):
    assert operator.keyring == keyring


async def test_license(operator, license):
    assert operator.license == license


async def test_raft(operator, raft):
    assert operator.raft == raft


async def test_segment(operator, segment):
    assert operator.segment == segment
