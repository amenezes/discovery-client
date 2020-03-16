import json

import discovery


def test_service_with_check():
    resp = discovery.service(
        "myapp", 5000, check=discovery.http("http://localhost:5000/health")
    )
    resp = json.loads(resp)
    assert tuple(["name", "id", "address", "port", "tags", "meta", "check"]) == tuple(
        resp
    )


def test_service_with_multi_check():
    resp = discovery.service(
        "myapp",
        5000,
        check=[
            discovery.http("http://localhost:5000/health"),
            discovery.tcp("localhost:22"),
        ],
    )
    assert tuple(["name", "id", "address", "port", "tags", "meta", "checks"]) == tuple(
        json.loads(resp)
    )


def test_create_service_without_check():
    resp = discovery.service("myapp2", 5001)
    assert "check" not in resp


def test_json():
    resp = discovery.service("myapp2", 5001)
    assert tuple(["name", "id", "address", "port", "tags", "meta"]) == tuple(
        json.loads(resp)
    )


def test_alias_check():
    resp = discovery.alias("myapp", "other_service_id")
    assert tuple(["name", "service_id", "alias_service"]) == tuple(resp)


def test_script_check():
    resp = discovery.script(["/usr/local/bin/check_mem.py", "-limit", "256MB"])
    assert tuple(["args", "interval", "timeout", "name"]) == tuple(resp)


def test_http_check():
    resp = discovery.http("http://localhost:5000/manage/health")
    assert tuple(
        [
            "http",
            "tls_skip_verify",
            "method",
            "header",
            "body",
            "interval",
            "timeout",
            "deregister_critical_service_after",
            "name",
        ]
    ) == tuple(resp)


def test_tcp_check():
    resp = discovery.tcp("localhost:22")
    assert tuple(["tcp", "interval", "timeout", "name"]) == tuple(resp)


def test_ttl_check():
    resp = discovery.ttl("my custom ttl", "30s")
    assert tuple(["notes", "ttl", "name"]) == tuple(resp)


def test_docker_check():
    resp = discovery.docker(
        container_id="f972c95ebf0e", args=["/usr/local/bin/check_mem.py"]
    )
    assert tuple(["docker_container_id", "shell", "args", "interval", "name"]) == tuple(
        resp.keys()
    )


def test_grpc_check():
    resp = discovery.grpc("127.0.0.1:12345")
    assert tuple(["grpc", "grpc_use_tls", "interval", "name"]) == tuple(resp)
