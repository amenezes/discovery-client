from typing import List, Optional
from uuid import uuid4


def script(
    args: List[str],
    name: Optional[str] = None,
    interval: str = "10s",
    timeout: str = "5s",
) -> dict:
    name = name or f"script-{uuid4().hex}"
    return dict(name=name, args=args, interval=interval, timeout=timeout)


def http(
    url: str,
    name: Optional[str] = None,
    tls_skip_verify: bool = True,
    tls_server_name: str = "",
    method: str = "GET",
    header: Optional[dict] = None,
    body: str = "",
    interval: str = "10s",
    timeout: str = "5s",
    deregister_after: str = "1m",
    disable_redirects: bool = True,
) -> dict:
    name = name or f"http-{uuid4().hex}"
    header = header or {}
    return dict(
        name=name,
        http=url,
        tls_server_name=tls_server_name,
        tls_skip_verify=tls_skip_verify,
        method=method,
        header=header,
        body=body,
        disable_redirects=disable_redirects,
        interval=interval,
        timeout=timeout,
        deregister_critical_service_after=deregister_after,
    )


def tcp(
    tcp_check: str,
    name: Optional[str] = None,
    interval: str = "10s",
    timeout: str = "5s",
) -> dict:
    name = name or f"tcp-{uuid4().hex}"
    return dict(name=name, tcp=tcp_check, interval=interval, timeout=timeout)


def ttl(notes: str, name: Optional[str] = None, ttl_check: str = "30s") -> dict:
    name = name or f"ttl-{uuid4().hex}"
    return dict(name=name, notes=notes, ttl=ttl_check)


def docker(
    container_id: str,
    args: str,
    shell: Optional[str] = None,
    name: Optional[str] = None,
    interval: str = "10s",
) -> dict:
    name = name or f"docker-{uuid4().hex}"
    return dict(
        name=name,
        docker_container_id=container_id,
        shell=shell,
        args=args,
        interval=interval,
    )


def grpc(
    grpc_check: str, name: Optional[str] = None, tls: bool = True, interval: str = "10s"
) -> dict:
    name = name or f"grpc-{uuid4().hex}"
    return dict(name=name, grpc=grpc_check, grpc_use_tls=tls, interval=interval)


def h2ping(
    h2ping_check: str,
    name: Optional[str] = None,
    interval: str = "10s",
    tls: bool = False,
) -> dict:
    check_id = f"h2ping-{uuid4().hex}"
    name = name or check_id
    return dict(
        id=check_id,
        name=name,
        h2ping=h2ping_check,
        interval=interval,
        h2ping_use_tls=tls,
    )


def alias(
    service_id: str,
    alias_service: str,
    alias_node: Optional[str] = None,
    name: Optional[str] = None,
) -> dict:
    """Consul's alias check.

    Usage:
    checks.alias('webapp1', 'webapp1-c5a5a6f40d7243ef84c8439b093de962')

    :param service_id: service name as registered in the Consul's catalog.
    :param alias_service: ServiceID of service registered in the Consul's catalog.
    :param alias_node: if the service is not registered with the same agent, "alias_node": "<node_id>" must also be specified.
    :param name: health check name.
    """
    name = name or f"alias-{uuid4().hex}"
    resp = dict(name=name, service_id=service_id, alias_service=alias_service)
    if alias_node:
        resp.update({"alias_node": alias_node})
    return resp
