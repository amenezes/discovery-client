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
    return json.dumps(response)


@singledispatch
def register_check(check):
    response = {"check": check}
    return response


@register_check.register(list)
def _(check):
    response = {"checks": []}
    for chk in check:
        response["checks"].append(chk)
    return response
