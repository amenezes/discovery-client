import json

import pytest


def sample_payload():
    return json.dumps({"Key": "3lg9DxVfKNzI8O+IQ5Ek+Q=="})


def sample_response():
    return [
        {
            "WAN": True,
            "Datacenter": "dc1",
            "Segment": "",
            "Keys": {
                "pUqJrVyVRj5jsiYEkM/tFQYfWyJIv4s3XkvDwy7Cu5s=": 1,
                "ZWTL+bgjHyQPhJRKcFe3ccirc2SFHmc/Nw67l8NQfdk=": 1,
                "WbL6oaTPom+7RG7Q/INbJWKy09OLar/Hf2SuOAdoQE4=": 1,
            },
            "NumNodes": 1,
        },
        {
            "WAN": False,
            "Datacenter": "dc1",
            "Segment": "",
            "Keys": {
                "pUqJrVyVRj5jsiYEkM/tFQYfWyJIv4s3XkvDwy7Cu5s=": 1,
                "ZWTL+bgjHyQPhJRKcFe3ccirc2SFHmc/Nw67l8NQfdk=": 1,
                "WbL6oaTPom+7RG7Q/INbJWKy09OLar/Hf2SuOAdoQE4=": 1,
            },
            "NumNodes": 1,
        },
    ]


@pytest.mark.parametrize("expected", [sample_response()])
async def test_list_keys(keyring, expected):
    keyring.client.expected = expected
    response = await keyring.list_keys()
    assert response == sample_response()


async def test_add_encryption_key(keyring, mocker):
    spy = mocker.spy(keyring.client, "post")
    await keyring.add_encryption_key(sample_payload())
    spy.assert_called_with(
        "/v1/operator/keyring", json={"Key": '{"Key": "3lg9DxVfKNzI8O+IQ5Ek+Q=="}'}
    )


async def test_change_encryption_key(keyring, mocker):
    spy = mocker.spy(keyring.client, "put")
    await keyring.change_encryption_key(sample_payload())
    spy.assert_called_with(
        "/v1/operator/keyring", json={"Key": '{"Key": "3lg9DxVfKNzI8O+IQ5Ek+Q=="}'}
    )


async def test_delete_encryption_key(keyring, mocker):
    spy = mocker.spy(keyring.client, "delete")
    await keyring.delete_encryption_key(sample_payload())
    spy.assert_called_with(
        "/v1/operator/keyring", json={"Key": '{"Key": "3lg9DxVfKNzI8O+IQ5Ek+Q=="}'}
    )
