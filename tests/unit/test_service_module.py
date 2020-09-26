import json

import pytest

from discovery.model.agent import checks
from discovery.model.agent.service import meta_is_valid, service, tags_is_valid


def test_service_with_check():
    resp = service("myapp", 5000, check=checks.http("http://localhost:5000/health"))
    resp = json.loads(resp)
    assert tuple(["name", "id", "address", "port", "tags", "meta", "check"]) == tuple(
        resp
    )


def test_service_with_multi_check():
    resp = service(
        "myapp",
        5000,
        check=[
            checks.http("http://localhost:5000/health"),
            checks.tcp("localhost:22"),
        ],
    )
    assert tuple(["name", "id", "address", "port", "tags", "meta", "checks"]) == tuple(
        json.loads(resp)
    )


def test_create_service_without_check():
    resp = service("myapp2", 5001)
    assert "check" not in resp


def test_json():
    resp = service("myapp2", 5001)
    assert tuple(["name", "id", "address", "port", "tags", "meta"]) == tuple(
        json.loads(resp)
    )


def test_alias_check():
    resp = checks.alias("myapp", "other_service_id")
    assert tuple(["name", "service_id", "aliasservice"]) == tuple(json.loads(resp))


def test_script_check():
    resp = checks.script(["/usr/local/bin/check_mem.py", "-limit", "256MB"])
    assert tuple(["args", "interval", "timeout", "name"]) == tuple(json.loads(resp))


def test_http_check():
    resp = checks.http("http://localhost:5000/manage/health")
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
    ) == tuple(json.loads(resp))


def test_tcp_check():
    resp = checks.tcp("localhost:22")
    assert tuple(["tcp", "interval", "timeout", "name"]) == tuple(json.loads(resp))


def test_ttl_check():
    resp = checks.ttl("my custom ttl", "30s")
    assert tuple(["notes", "ttl", "name"]) == tuple(json.loads(resp))


def test_docker_check():
    resp = checks.docker(
        container_id="f972c95ebf0e", args=["/usr/local/bin/check_mem.py"]
    )
    assert tuple(["docker_container_id", "shell", "args", "interval", "name"]) == tuple(
        json.loads(resp).keys()
    )


def test_grpc_check():
    resp = checks.grpc("127.0.0.1:12345")
    assert tuple(["grpc", "grpc_use_tls", "interval", "name"]) == tuple(
        json.loads(resp)
    )


def test_tags_validation():
    tags_is_valid(["python", "ia"])


def test_invalid_tags():
    with pytest.raises(ValueError):
        tags_is_valid("python")


def test_metadata_validation():
    meta_is_valid({"lang": "python", "env": "production"})


def test_invalid_metadata():
    with pytest.raises(ValueError):
        meta_is_valid("python")
