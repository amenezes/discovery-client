import collections
import random
import socket
import uuid
from dataclasses import asdict, dataclass
from functools import singledispatch
from typing import List, Optional, Union


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
            return None


rr_services = _InnerServices()


def select_one_random(services: str):
    service_selected = random.randint(0, (len(services) - 1))
    return services[service_selected]


def select_one_rr(services: str):
    key_ = uuid.uuid5(uuid.NAMESPACE_DNS, str(services)).hex
    rr_services.add(key_, services)
    return rr_services.get(key_)


@dataclass
class Service:
    name: str
    port: int
    id: Optional[str] = None
    address: Optional[str] = None
    tags: Optional[List[str]] = None
    meta: Optional[dict] = None
    enable_tag_override: bool = False
    weights: Optional[dict] = None
    check: Optional[Union[dict, List[dict]]] = None

    def __post_init__(self):
        self.id = self.id or f"{self.name}-{uuid.uuid4().hex}"
        self.address = self.address or f"{socket.gethostbyname(socket.gethostname())}"
        self.meta = self.meta or {}
        self.tags = self.tags or []
        tags_is_valid(self.tags)
        meta_is_valid(self.meta)

    def dict(self) -> dict:
        data = asdict(self)
        if self.check:
            data.update(register_check(self.check))
        return data

    def __getitem__(self, key: str):
        return self.__dict__[key]


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
