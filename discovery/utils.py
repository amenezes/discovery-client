import collections
import random
import uuid

__rr_services = {}  # type: ignore
# Temporarily


def select_one_random(services):
    service_selected = random.randint(0, (len(services) - 1))
    return services[service_selected]


def select_one_rr(services):
    global __rr_services
    key_ = uuid.uuid5(uuid.NAMESPACE_DNS, str(services)).hex
    if key_ not in __rr_services.keys() or len(__rr_services.get(key_)) == 0:
        __rr_services.update({key_: collections.deque(services)})

    return __rr_services.get(key_).popleft()
