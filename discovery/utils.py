"""Module of utilitarian methods."""

import collections
import random


__rr_services = collections.deque()


def select_one_randomly(services):
    """Select one service randomly."""
    service_selected = random.randint(0, (len(services)-1))
    return services[service_selected]


def select_one_rr(services):
    """Select one service using round robin algorithm."""
    global __rr_services

    if len(__rr_services) == 0:
        __rr_services = collections.deque(services)
    return __rr_services.popleft()
