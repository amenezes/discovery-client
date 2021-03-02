import collections
import random
import socket
import uuid
from functools import singledispatch
from typing import List, Optional

from discovery import exceptions


class _InnerServices:
    def __init__(self):
        self.services = {}

    def add(self, key, value) -> None:
        if key not in self.services or len(self.services.get(key)) == 0:
            self.services.update({key: collections.deque(value)})

    def get(self, value):
        try:
            return self.services.get(value).popleft()
        except IndexError:
            raise exceptions.ServiceNotFoundException(
                "Service not found in the Consul's catalog."
            )


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
    service_id: Optional[str] = None,
    address: Optional[str] = None,
    tags: Optional[List[str]] = None,
    meta: Optional[dict] = None,
    proxy: Optional[str] = None,
    connect: Optional[str] = None,
    enable_tag_override: bool = False,
    weights: Optional[dict] = None,
    check: Optional[dict] = None,
) -> dict:
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
        "EnableTagOverride": enable_tag_override,
        "Weights": weights,
    }
    if check:
        response.update(register_check(check))
    return response


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
    return {"check": check}


@register_check.register(list)
def _(check) -> dict:
    return {"checks": check}
