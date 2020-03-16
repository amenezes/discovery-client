from uuid import uuid4


def script(args, name=None, interval="10s", timeout="5s"):
    script_id = f"script-{uuid4().hex}"
    name = name or script_id
    response = {"args": args, "interval": interval, "timeout": timeout, "name": name}
    return response


def http(
    url,
    name=None,
    tls_skip_verify=True,
    method="GET",
    header={},
    body="",
    interval="10s",
    timeout="5s",
    deregister_after="1m",
):
    http_id = f"http-{uuid4().hex}"
    name = name or http_id
    response = {
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
    return response


def tcp(tcp, name=None, interval="10s", timeout="5s"):
    tcp_id = f"tcp-{uuid4().hex}"
    name = name or tcp_id
    response = {"tcp": tcp, "interval": interval, "timeout": timeout, "name": name}
    return response


def ttl(notes, name=None, ttl="30s"):
    ttl_id = f"ttl-{uuid4().hex}"
    name = name or ttl_id
    response = {"notes": notes, "ttl": ttl, "name": name}
    return response


def docker(container_id, args, shell=None, name=None, interval="10s"):
    docker_id = f"docker-{uuid4().hex}"
    name = name or docker_id
    response = {
        "docker_container_id": container_id,
        "shell": shell,
        "args": args,
        "interval": interval,
        "name": name,
    }
    return response


def grpc(grpc, name=None, tls=True, interval="10s"):
    grpc_id = f"grpc-{uuid4().hex}"
    name = name or grpc_id
    response = {"grpc": grpc, "grpc_use_tls": tls, "interval": interval, "name": name}
    return response


def alias(service_id, alias_service, name=None):
    """Consul's alias check.

    alias_service: backend
    service_id: frontent
    """
    name = name or f"alias-{uuid4().hex}"
    return {
        "name": name,
        "service_id": service_id,
        "alias_service": alias_service,
    }
