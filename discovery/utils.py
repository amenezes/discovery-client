"""Module of utilitarian methods."""

import collections
import random


__rr_services = {}


def select_one_randomly(services):
    """Select one service randomly."""
    service_selected = random.randint(0, (len(services) - 1))
    return services[service_selected]


def select_one_rr(service_name, services):
    """Select one service using round robin algorithm."""
    global __rr_services

    if len(services) == 0:
        raise IndexError(f'Service: <{service_name}> not found!')
    elif service_name not in __rr_services.keys() or len(__rr_services.get(service_name)) == 0:
        __rr_services.update({service_name: collections.deque(services)})

    return __rr_services.get(service_name).popleft()
