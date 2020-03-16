from unittest.mock import MagicMock, patch

import aiohttp
import pytest

from discovery import api
from tests.unit.setup import consul_api


def sample_response():
    return ["", "alpha", "beta"]


@pytest.fixture
@pytest.mark.asyncio
async def segment(consul_api):
    return api.Segment(client=consul_api)


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [sample_response()])
async def test_list(segment, expected):
    segment.client.expected = expected
    response = await segment.list()
    resp = await response.json()
    assert resp == sample_response()
