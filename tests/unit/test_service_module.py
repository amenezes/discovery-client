import pytest

from discovery import checks, utils
from discovery.utils import Service


def test_service_with_check():
    svc = Service("myapp", 5000, check=checks.http("http://localhost:5000/health"))
    assert svc["check"] is not None


def test_service_with_multi_check():
    svc = Service(
        "myapp",
        5000,
        check=[
            checks.http("http://localhost:5000/health"),
            checks.tcp("localhost:22"),
        ],
    )
    assert len(svc["check"]) == 2


def test_create_service_without_check():
    svc = Service("myapp2", 5001)
    assert hasattr(svc, "check")


def test_service_return():
    svc = Service("myapp2", 5001)
    assert isinstance(svc, Service)


@pytest.mark.parametrize("prop", ["name", "service_id", "alias_service"])
def test_alias_check(prop):
    assert prop in checks.alias("myapp", "other_service_id")


@pytest.mark.parametrize("prop", ["args", "interval", "timeout", "name"])
def test_script_check(prop):
    assert prop in checks.script(["/usr/local/bin/check_mem.py", "-limit", "256MB"])


@pytest.mark.parametrize("prop", ["id", "name", "h2ping", "interval", "h2ping_use_tls"])
def test_h2ping_check(prop):
    assert prop in checks.h2ping([])


@pytest.mark.parametrize(
    "prop",
    [
        "http",
        "tls_skip_verify",
        "tls_server_name",
        "method",
        "header",
        "body",
        "interval",
        "timeout",
        "deregister_critical_service_after",
        "disable_redirects",
        "name",
    ],
)
def test_http_check(prop):
    assert prop in checks.http("http://localhost:5000/manage/health")


@pytest.mark.parametrize("prop", ["tcp", "interval", "timeout", "name"])
def test_tcp_check(prop):
    assert prop in checks.tcp("localhost:22")


@pytest.mark.parametrize("prop", ["notes", "ttl", "name"])
def test_ttl_check(prop):
    assert prop in checks.ttl("my custom ttl", "30s")


@pytest.mark.parametrize(
    "prop", ["docker_container_id", "shell", "args", "interval", "name"]
)
def test_docker_check(prop):
    assert prop in checks.docker(
        container_id="f972c95ebf0e", args=["/usr/local/bin/check_mem.py"]
    )


@pytest.mark.parametrize("prop", ["grpc", "grpc_use_tls", "interval", "name"])
def test_grpc_check(prop):
    assert prop in checks.grpc("127.0.0.1:12345")


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
