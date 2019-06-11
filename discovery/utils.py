"""Module of utilitarian methods."""

import collections
import random


__rr_services = {}


def select_one_random(services):
    """Select one service randomly."""
    service_selected = random.randint(0, (len(services) - 1))
    return services[service_selected]


def select_one_rr(services):
    """Select one service using round robin algorithm."""
    global __rr_services
    key_ = id(services)

    if len(services) == 0:
        raise IndexError('Services must be greater than zero.')
    if key_ not in __rr_services.keys() or len(__rr_services.get(key_)) == 0:
        __rr_services.update(
            {key_: collections.deque(services)})

    return __rr_services.get(key_).popleft()
