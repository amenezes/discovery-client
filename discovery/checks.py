import json
from typing import Optional
from uuid import uuid4


def script(
    args: str, name: Optional[str] = None, interval: str = "10s", timeout: str = "5s"
) -> str:
    script_id = f"script-{uuid4().hex}"
    name = name or script_id
    return json.dumps(
        {"args": args, "interval": interval, "timeout": timeout, "name": name}
    )


def http(
    url,
    name=None,
    tls_skip_verify: bool = True,
    method: str = "GET",
    header: dict = {},
    body: str = "",
    interval: str = "10s",
    timeout: str = "5s",
    deregister_after: str = "1m",
) -> str:
    http_id = f"http-{uuid4().hex}"
    name = name or http_id
    return json.dumps(
        {
            "http": url,
            "tls_skip_verify": tls_skip_verify,
            "method": method,
            "header": header,
            "body": body,
            "interval": interval,
            "timeout": timeout,
            "deregister_critical_service_after": deregister_after,
            "name": name,
        }
    )


def tcp(
    tcp, name: Optional[str] = None, interval: str = "10s", timeout: str = "5s"
) -> str:
    tcp_id = f"tcp-{uuid4().hex}"
    name = name or tcp_id
    return json.dumps(
        {"tcp": tcp, "interval": interval, "timeout": timeout, "name": name}
    )


def ttl(notes: str, name: Optional[str] = None, ttl: str = "30s") -> str:
    ttl_id = f"ttl-{uuid4().hex}"
    name = name or ttl_id
    return json.dumps({"notes": notes, "ttl": ttl, "name": name})


def docker(
    container_id: str,
    args: str,
    shell: Optional[str] = None,
    name: Optional[str] = None,
    interval: str = "10s",
) -> str:
    docker_id = f"docker-{uuid4().hex}"
    name = name or docker_id
    return json.dumps(
        {
            "docker_container_id": container_id,
            "shell": shell,
            "args": args,
            "interval": interval,
            "name": name,
        }
    )


def grpc(
    grpc: str, name: Optional[str] = None, tls: bool = True, interval: str = "10s"
) -> str:
    grpc_id = f"grpc-{uuid4().hex}"
    name = name or grpc_id
    return json.dumps(
        {"grpc": grpc, "grpc_use_tls": tls, "interval": interval, "name": name}
    )


def alias(service_id: str, alias_service: str, name: Optional[str] = None) -> str:
    """Consul's alias check.

    alias_service: backend
    service_id: frontent
    """
    name = name or f"alias-{uuid4().hex}"
    return json.dumps(
        {"name": name, "service_id": service_id, "aliasservice": alias_service}
    )
