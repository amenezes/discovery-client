import pytest


def sample_response():
    return ["", "alpha", "beta"]


@pytest.mark.parametrize("expected", [sample_response()])
async def test_list(segment, expected):
    segment.client.expected = expected
    resp = await segment.list()
    assert resp == sample_response()
