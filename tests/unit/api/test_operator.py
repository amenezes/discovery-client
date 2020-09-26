import pytest

from discovery import api


@pytest.fixture
@pytest.mark.asyncio
async def operator(consul_api, area, autopilot, keyring, license, raft, segment):
    return api.Operator(
        area, autopilot, keyring, license, raft, segment, client=consul_api,
    )


@pytest.mark.asyncio
async def test_area(operator, area):
    assert operator.area == area


@pytest.mark.asyncio
async def test_autopilot(operator, autopilot):
    assert operator.autopilot == autopilot


@pytest.mark.asyncio
async def test_keyring(operator, keyring):
    assert operator.keyring == keyring


@pytest.mark.asyncio
async def test_license(operator, license):
    assert operator.license == license


@pytest.mark.asyncio
async def test_raft(operator, raft):
    assert operator.raft == raft


@pytest.mark.asyncio
async def test_segment(operator, segment):
    assert operator.segment == segment
