import pytest

from discovery.utils import select_one_random, select_one_rr


@pytest.fixture
def services():
    return ["a", "b", "c"]


def test_select_one_random(services):
    for service in services:
        assert select_one_random(services) in services


def test_select_one_rr(services):
    # group 1: select single service
    for service in services:
        assert select_one_rr(service) == service

    # group 2: select alternate services
    servicesB = ["a", "b"]
    servicesC = ["c", "d", "e"]

    # B service
    assert select_one_rr(servicesB) == "a"
    assert select_one_rr(servicesB) == "b"
    assert select_one_rr(servicesB) == "a"
    # C service
    assert select_one_rr(servicesC) == "c"
    assert select_one_rr(servicesC) == "d"
    assert select_one_rr(servicesC) == "e"
    assert select_one_rr(servicesC) == "c"
