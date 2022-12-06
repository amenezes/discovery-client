import pytest

from discovery import api


def update_response():
    return {
        "ID": "000ed53c-e2d3-e7e6-31a5-c19bc3518a3d",
        "Description": "updated rule",
        "AuthMethod": "minikube",
        "Selector": "serviceaccount.namespace=dev",
        "BindType": "role",
        "BindName": "{{ serviceaccount.name }}",
        "CreateIndex": 17,
        "ModifyIndex": 18,
    }


def sample_response():
    return {
        "ID": "000ed53c-e2d3-e7e6-31a5-c19bc3518a3d",
        "Description": "example rule",
        "AuthMethod": "minikube",
        "Selector": "serviceaccount.namespace==default",
        "BindType": "service",
        "BindName": "{{ serviceaccount.name }}",
        "CreateIndex": 17,
        "ModifyIndex": 17,
    }


def list_binding_response():
    return [
        {
            "ID": "000ed53c-e2d3-e7e6-31a5-c19bc3518a3d",
            "Description": "example 1",
            "AuthMethod": "minikube-1",
            "BindType": "service",
            "BindName": "k8s-{{ serviceaccount.name }}",
            "CreateIndex": 17,
            "ModifyIndex": 17,
        },
        {
            "ID": "b4f0a0a3-69f2-7a4f-6bef-326034ace9fa",
            "Description": "example 2",
            "AuthMethod": "minikube-2",
            "Selector": "serviceaccount.namespace==default",
            "BindName": "k8s-{{ serviceaccount.name }}",
            "CreateIndex": 18,
            "ModifyIndex": 18,
        },
    ]


@pytest.fixture
async def binding_rule(consul_api):
    return api.BindingRule(client=consul_api)


@pytest.mark.parametrize("expected", [sample_response()])
async def test_create(binding_rule, expected):
    binding_rule.client.expected = expected
    response = await binding_rule.create(
        "minikube", "service", r"{{ serviceaccount.name }}"
    )
    assert response == sample_response()


@pytest.mark.parametrize("expected", [sample_response()])
async def test_read(binding_rule, expected):
    binding_rule.client.expected = expected
    response = await binding_rule.read("000ed53c-e2d3-e7e6-31a5-c19bc3518a3d")
    assert response == sample_response()


@pytest.mark.parametrize("expected", [update_response()])
async def test_update(binding_rule, expected):
    binding_rule.client.expected = expected
    response = await binding_rule.update(
        "000ed53c-e2d3-e7e6-31a5-c19bc3518a3d",
        "minikube",
        "role",
        r"{{ serviceaccount.name }}",
    )
    assert response == update_response()


async def test_delete(binding_rule):
    binding_rule.client.expected = True
    response = await binding_rule.delete("000ed53c-e2d3-e7e6-31a5-c19bc3518a3d")
    assert response


@pytest.mark.parametrize("expected", [list_binding_response()])
async def test_list(binding_rule, expected):
    binding_rule.client.expected = expected
    response = await binding_rule.list()
    assert response == list_binding_response()
