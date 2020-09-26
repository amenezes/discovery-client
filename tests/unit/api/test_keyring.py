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


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [sample_response()])
async def test_list(keyring, expected):
    keyring.client.expected = expected
    response = await keyring.list()
    response = await response.json()
    assert response == sample_response()


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_add(keyring, expected):
    keyring.client.expected = expected
    response = await keyring.add(sample_payload())
    assert response.status == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_change(keyring, expected):
    keyring.client.expected = expected
    response = await keyring.change(sample_payload())
    assert response.status == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("expected", [200])
async def test_delete(keyring, expected):
    keyring.client.expected = expected
    response = await keyring.delete(sample_payload())
    assert response.status == 200
