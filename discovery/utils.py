import collections
import random
import uuid


class _InnerServices:
    def __init__(self):
        self.services = {}

    def add(self, key, value):
        if key not in self.services or len(self.services.get(key)) == 0:
            self.services.update({key: collections.deque(value)})

    def get(self, value):
        return self.services.get(value).popleft()


rr_services = _InnerServices()


def select_one_random(services):
    service_selected = random.randint(0, (len(services) - 1))
    return services[service_selected]


def select_one_rr(services):
    key_ = uuid.uuid5(uuid.NAMESPACE_DNS, str(services)).hex
    rr_services.add(key_, services)
    return rr_services.get(key_)
