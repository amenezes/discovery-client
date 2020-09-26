import json
import socket
from functools import singledispatch
from uuid import uuid4


def service(
    name,
    port,
    dc="",
    address=None,
    tags=None,
    meta=None,
    namespace="default",
    check=None,
):
    service_id = f"{name}-{uuid4().hex}"
    address = address = f"{socket.gethostbyname(socket.gethostname())}"
    meta = meta or {}
    tags = tags or []
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
    tags_is_valid(tags)
    meta_is_valid(meta)
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
