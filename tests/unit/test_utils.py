import pytest

from discovery.exceptions import ServiceNotFoundException
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
    servicesB = ["d", "e"]
    servicesC = ["f", "g", "h"]

    assert select_one_rr(servicesB) == "d"
    assert select_one_rr(servicesC) == "f"
    assert select_one_rr(servicesC) == "g"
    assert select_one_rr(servicesB) == "e"
    assert select_one_rr(servicesB) == "d"
    assert select_one_rr(servicesC) == "h"
    assert select_one_rr(servicesC) == "f"


def test_select_one_rr_exception():
    with pytest.raises(ServiceNotFoundException):
        select_one_rr([])
