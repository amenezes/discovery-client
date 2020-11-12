import collections
import json
import random
import socket
import uuid
from functools import singledispatch
from typing import Optional


class _InnerServices:
    def __init__(self):
        self.services = {}

    def add(self, key, value) -> None:
        if key not in self.services or len(self.services.get(key)) == 0:
            self.services.update({key: collections.deque(value)})

    def get(self, value):
        return self.services.get(value).popleft()


rr_services = _InnerServices()


def select_one_random(services: str):
    service_selected = random.randint(0, (len(services) - 1))
    return services[service_selected]


def select_one_rr(services: str):
    key_ = uuid.uuid5(uuid.NAMESPACE_DNS, str(services)).hex
    rr_services.add(key_, services)
    return rr_services.get(key_)


def service(
    name: str,
    port: int,
    dc: str = "",
    service_id: Optional[str] = None,
    address: Optional[str] = None,
    tags: Optional[list] = None,
    meta: Optional[dict] = None,
    namespace: str = "default",
    check: Optional[str] = None,
) -> str:
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


def tags_is_valid(tags: Optional[list]) -> bool:
    if not isinstance(tags, list):
        raise ValueError("tags must be list")
    return True


def meta_is_valid(meta: Optional[dict]) -> bool:
    if not isinstance(meta, dict):
        raise ValueError("meta must be dict")
    return True


@singledispatch
def register_check(check) -> dict:
    response = {"check": json.loads(check)}
    return response


@register_check.register(list)
def _(check) -> dict:
    response: dict = {"checks": []}
    for chk in check:
        response["checks"].append(json.loads(chk))
    return response
