import pytest


def sample_response():
    return ["", "alpha", "beta"]


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [sample_response()])
async def test_list(segment, expected):
    segment.client.expected = expected
    response = await segment.list()
    resp = await response.json()
    assert resp == sample_response()
