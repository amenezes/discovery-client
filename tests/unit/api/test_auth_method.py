import json

import pytest

from discovery import api
from tests.unit.setup import consul_api


def create_payload():
    return json.dumps(
        {
            "Name": "minikube",
            "Type": "kubernetes",
            "Description": "dev minikube cluster",
            "Config": {
                "Host": "https://192.0.2.42:8443",
                "CACert": "-----BEGIN CERTIFICATE-----\n...-----END CERTIFICATE-----\n",
                "ServiceAccountJWT": "eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9...",
            },
        }
    )


def create_response():
    return {
        "Name": "minikube",
        "Type": "kubernetes",
        "Description": "dev minikube cluster",
        "Config": {
            "Host": "https://192.0.2.42:8443",
            "CACert": "-----BEGIN CERTIFICATE-----\n...-----END CERTIFICATE-----\n",
            "ServiceAccountJWT": "eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9...",
        },
        "CreateIndex": 15,
        "ModifyIndex": 15,
    }


def read_response():
    return {
        "Name": "minikube",
        "Type": "kubernetes",
        "Description": "dev minikube cluster",
        "Config": {
            "Host": "https://192.0.2.42:8443",
            "CACert": "-----BEGIN CERTIFICATE-----\n...-----END CERTIFICATE-----\n",
            "ServiceAccountJWT": "eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9...",
        },
        "CreateIndex": 15,
        "ModifyIndex": 224,
    }


def update_payload():
    return {
        "Name": "minikube",
        "Description": "updated name",
        "Config": {
            "Host": "https://192.0.2.42:8443",
            "CACert": "-----BEGIN CERTIFICATE-----\n...-----END CERTIFICATE-----\n",
            "ServiceAccountJWT": "eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9...",
        },
    }


def update_response():
    return {
        "Name": "minikube",
        "Description": "updated name",
        "Type": "kubernetes",
        "Config": {
            "Host": "https://192.0.2.42:8443",
            "CACert": "-----BEGIN CERTIFICATE-----\n...-----END CERTIFICATE-----\n",
            "ServiceAccountJWT": "eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9...",
        },
        "CreateIndex": 15,
        "ModifyIndex": 224,
    }


def list_response():
    return [
        {
            "Name": "minikube-1",
            "Type": "kubernetes",
            "Description": "",
            "CreateIndex": 14,
            "ModifyIndex": 14,
        },
        {
            "Name": "minikube-2",
            "Type": "kubernetes",
            "Description": "",
            "CreateIndex": 15,
            "ModifyIndex": 15,
        },
    ]


@pytest.fixture
@pytest.mark.asyncio
async def auth_method(consul_api):
    return api.AuthMethod(client=consul_api)


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [create_response()])
async def test_create(auth_method, expected):
    auth_method.client.expected = expected
    response = await auth_method.create(create_payload())
    response = await response.json()
    assert response == create_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [read_response()])
async def test_read(auth_method, expected):
    auth_method.client.expected = expected
    response = await auth_method.read("minikube")
    response = await response.json()
    assert response == read_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [update_response()])
async def test_update(auth_method, expected):
    auth_method.client.expected = expected
    response = await auth_method.update("minikube", update_payload())
    response = await response.json()
    assert response == update_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_delete(auth_method, expected):
    auth_method.client.expected = expected
    response = await auth_method.delete("minikube")
    assert response.status == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [list_response()])
async def test_list(auth_method, expected):
    auth_method.client.expected = expected
    response = await auth_method.list()
    response = await response.json()
    assert response == list_response()
