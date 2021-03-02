import pytest

from discovery import check, service, utils


def test_service_with_check():
    resp = service("myapp", 5000, check=check.http("http://localhost:5000/health"))
    assert resp["check"] is not None


def test_service_with_multi_check():
    resp = service(
        "myapp",
        5000,
        check=[
            check.http("http://localhost:5000/health"),
            check.tcp("localhost:22"),
        ],
    )
    assert len(resp["checks"]) == 2


def test_create_service_without_check():
    resp = service("myapp2", 5001)
    assert "check" not in resp


def test_service_return():
    resp = service("myapp2", 5001)
    assert isinstance(resp, dict)


def test_alias_check():
    resp = check.alias("myapp", "other_service_id")
    assert tuple(["name", "service_id", "aliasservice"]) == tuple(resp)


def test_script_check():
    resp = check.script(["/usr/local/bin/check_mem.py", "-limit", "256MB"])
    assert tuple(["args", "interval", "timeout", "name"]) == tuple(resp)


def test_http_check():
    resp = check.http("http://localhost:5000/manage/health")
    assert (
        tuple(
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
        )
        == tuple(resp)
    )


def test_tcp_check():
    resp = check.tcp("localhost:22")
    assert tuple(["tcp", "interval", "timeout", "name"]) == tuple(resp)


def test_ttl_check():
    resp = check.ttl("my custom ttl", "30s")
    assert tuple(["notes", "ttl", "name"]) == tuple(resp)


def test_docker_check():
    resp = check.docker(
        container_id="f972c95ebf0e", args=["/usr/local/bin/check_mem.py"]
    )
    assert tuple(["docker_container_id", "shell", "args", "interval", "name"]) == tuple(
        resp.keys()
    )


def test_grpc_check():
    resp = check.grpc("127.0.0.1:12345")
    assert tuple(["grpc", "grpc_use_tls", "interval", "name"]) == tuple(resp)


def test_tags_validation():
    utils.tags_is_valid(["python", "ia"])


def test_invalid_tags():
    with pytest.raises(ValueError):
        utils.tags_is_valid("python")


def test_metadata_validation():
    utils.meta_is_valid({"lang": "python", "env": "production"})


def test_invalid_metadata():
    with pytest.raises(ValueError):
        utils.meta_is_valid("python")
