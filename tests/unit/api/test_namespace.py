import json

import pytest

from discovery import api


def create_payload():
    return json.dumps(
        {
            "Name": "team-1",
            "Description": "Namespace for Team 1",
            "ACLs": {
                "PolicyDefaults": [
                    {"ID": "77117cf6-d976-79b0-d63b-5a36ac69c8f1"},
                    {"Name": "node-read"},
                ],
                "RoleDefaults": [
                    {"ID": "69748856-ae69-d620-3ec4-07844b3c6be7"},
                    {"Name": "ns-team-2-read"},
                ],
            },
            "Meta": {"foo": "bar"},
        }
    )


def create_response():
    return {
        "Name": "team-1",
        "Description": "Namespace for Team 1",
        "ACLs": {
            "PolicyDefaults": [
                {"ID": "77117cf6-d976-79b0-d63b-5a36ac69c8f1", "Name": "service-read"},
                {"ID": "af937401-9950-fcae-8396-610ce047649a", "Name": "node-read"},
            ],
            "RoleDefaults": [
                {
                    "ID": "69748856-ae69-d620-3ec4-07844b3c6be7",
                    "Name": "service-discovery",
                },
                {
                    "ID": "ae4b3542-d824-eb5f-7799-3fd657847e4e",
                    "Name": "ns-team-2-read",
                },
            ],
        },
        "Meta": {"foo": "bar"},
        "CreateIndex": 55,
        "ModifyIndex": 55,
    }


# def update_payload():
#     return {
#         "Description": "Namespace for Team 1",
#         "ACLs": {
#             "PolicyDefaults": [
#                 {"ID": "77117cf6-d976-79b0-d63b-5a36ac69c8f1"},
#                 {"Name": "node-read"},
#             ],
#             "RoleDefaults": [
#                 {"ID": "69748856-ae69-d620-3ec4-07844b3c6be7"},
#                 {"Name": "ns-team-2-read"},
#             ],
#         },
#         "Meta": {"foo": "bar"},
#     }


def update_response():
    return {
        "Name": "team-1",
        "Description": "Namespace for Team 1",
        "ACLs": {
            "PolicyDefaults": [
                {"ID": "77117cf6-d976-79b0-d63b-5a36ac69c8f1", "Name": "service-read"},
                {"ID": "af937401-9950-fcae-8396-610ce047649a", "Name": "node-read"},
            ],
            "RoleDefaults": [
                {
                    "ID": "69748856-ae69-d620-3ec4-07844b3c6be7",
                    "Name": "service-discovery",
                },
                {
                    "ID": "ae4b3542-d824-eb5f-7799-3fd657847e4e",
                    "Name": "ns-team-2-read",
                },
            ],
        },
        "Meta": {"foo": "bar"},
        "CreateIndex": 55,
        "ModifyIndex": 55,
    }


def delete_response():
    return {
        "Name": "team-1",
        "Description": "Namespace for Team 1",
        "ACLs": {
            "PolicyDefaults": [
                {"ID": "77117cf6-d976-79b0-d63b-5a36ac69c8f1", "Name": "service-read"},
                {"ID": "af937401-9950-fcae-8396-610ce047649a", "Name": "node-read"},
            ],
            "RoleDefaults": [
                {
                    "ID": "69748856-ae69-d620-3ec4-07844b3c6be7",
                    "Name": "service-discovery",
                },
                {
                    "ID": "ae4b3542-d824-eb5f-7799-3fd657847e4e",
                    "Name": "ns-team-2-read",
                },
            ],
        },
        "Meta": {"foo": "bar"},
        "DeletedAt": "2019-12-02T23:00:00Z",
        "CreateIndex": 55,
        "ModifyIndex": 100,
    }


def list_all_response():
    return [
        {
            "Name": "default",
            "Description": "Builtin Default Namespace",
            "CreateIndex": 6,
            "ModifyIndex": 6,
        },
        {
            "Name": "team-1",
            "Description": "Namespace for Team 1",
            "ACLs": {
                "PolicyDefaults": [
                    {
                        "ID": "77117cf6-d976-79b0-d63b-5a36ac69c8f1",
                        "Name": "service-read",
                    },
                    {"ID": "af937401-9950-fcae-8396-610ce047649a", "Name": "node-read"},
                ],
                "RoleDefaults": [
                    {
                        "ID": "69748856-ae69-d620-3ec4-07844b3c6be7",
                        "Name": "service-discovery",
                    },
                    {
                        "ID": "ae4b3542-d824-eb5f-7799-3fd657847e4e",
                        "Name": "ns-team-2-read",
                    },
                ],
            },
            "Meta": {"foo": "bar"},
            "CreateIndex": 55,
            "ModifyIndex": 55,
        },
    ]


@pytest.fixture
async def namespace(consul_api):
    return api.Namespace(client=consul_api)


@pytest.mark.parametrize("expected", [create_response()])
async def test_create(namespace, expected):
    namespace.client.expected = expected
    response = await namespace.create(create_payload())
    assert response == create_response()


@pytest.mark.parametrize("expected", [create_response()])
async def test_read(namespace, expected):
    namespace.client.expected = expected
    response = await namespace.read("team-1")
    assert response == create_response()


@pytest.mark.parametrize("expected", [update_response()])
async def test_update(namespace, expected):
    namespace.client.expected = expected
    response = await namespace.update("team-1", "Namespace for Team 1")
    assert response == update_response()


@pytest.mark.parametrize("expected", [delete_response()])
async def test_delete(namespace, expected):
    namespace.client.expected = expected
    response = await namespace.delete("team-1")
    assert response == delete_response()


@pytest.mark.parametrize("expected", [list_all_response()])
async def test_list_all(namespace, expected):
    namespace.client.expected = expected
    response = await namespace.list_all()
    assert response == list_all_response()
