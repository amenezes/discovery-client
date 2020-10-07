import collections
import json
import random
import socket
import uuid
from functools import singledispatch


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


def service(
    name,
    port,
    dc="",
    service_id=None,
    address=None,
    tags=None,
    meta=None,
    namespace="default",
    check=None,
):
    service_id = service_id or f"{name}-{uuid.uuid4().hex}"
    address = address or f"{socket.gethostbyname(socket.gethostname())}"
    meta = meta or {}
    tags = tags or []
    tags_is_valid(tags)
    meta_is_valid(meta)
    response = {
        "name": name,
        "id": service_id,
        "address": address,
        "port": port,
        "tags": tags,
        "meta": meta,
    }
    if check:
        response.update(register_check(check))
    return json.dumps(response)


def tags_is_valid(tags):
    if not isinstance(tags, list):
        raise ValueError("tags must be list")
    return True


def meta_is_valid(meta):
    if not isinstance(meta, dict):
        raise ValueError("meta must be dict")
    return True


@singledispatch
def register_check(check):
    response = {"check": json.loads(check)}
    return response


@register_check.register(list)
def _(check):
    response = {"checks": []}
    for chk in check:
        response["checks"].append(json.loads(chk))
    return response
