from typing import Optional
from uuid import uuid4


def script(
    args: str, name: Optional[str] = None, interval: str = "10s", timeout: str = "5s"
) -> dict:
    script_id = f"script-{uuid4().hex}"
    name = name or script_id
    return {"args": args, "interval": interval, "timeout": timeout, "name": name}


def http(
    url: str,
    name: Optional[str] = None,
    tls_skip_verify: bool = True,
    method: str = "GET",
    header: Optional[dict] = None,
    body: str = "",
    interval: str = "10s",
    timeout: str = "5s",
    deregister_after: str = "1m",
) -> dict:
    http_id = f"http-{uuid4().hex}"
    name = name or http_id
    header = header or {}
    return {
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


def tcp(
    tcp, name: Optional[str] = None, interval: str = "10s", timeout: str = "5s"
) -> dict:
    tcp_id = f"tcp-{uuid4().hex}"
    name = name or tcp_id
    return {"tcp": tcp, "interval": interval, "timeout": timeout, "name": name}


def ttl(notes: str, name: Optional[str] = None, ttl: str = "30s") -> dict:
    ttl_id = f"ttl-{uuid4().hex}"
    name = name or ttl_id
    return {"notes": notes, "ttl": ttl, "name": name}


def docker(
    container_id: str,
    args: str,
    shell: Optional[str] = None,
    name: Optional[str] = None,
    interval: str = "10s",
) -> dict:
    docker_id = f"docker-{uuid4().hex}"
    name = name or docker_id
    return {
        "docker_container_id": container_id,
        "shell": shell,
        "args": args,
        "interval": interval,
        "name": name,
    }


def grpc(
    grpc: str, name: Optional[str] = None, tls: bool = True, interval: str = "10s"
) -> dict:
    grpc_id = f"grpc-{uuid4().hex}"
    name = name or grpc_id
    return {"grpc": grpc, "grpc_use_tls": tls, "interval": interval, "name": name}


def alias(
    service_id: str,
    alias_service: str,
    alias_node: Optional[str] = None,
    name: Optional[str] = None,
) -> dict:
    """Consul's alias check.

    Usage:

        check.alias('webapp1', 'webapp1-c5a5a6f40d7243ef84c8439b093de962')

    :param service_id: service name as registered in the Consul's catalog.
    :param alias_service: ServiceID of service registered in the Consul's catalog.
    :param alias_node: if the service is not registered with the same agent, "alias_node": "<node_id>" must also be specified.
    """
    name = name or f"alias-{uuid4().hex}"
    resp = {"name": name, "service_id": service_id, "aliasservice": alias_service}
    if alias_node is not None:
        resp.update({"aliasnode": alias_node})
    return resp
