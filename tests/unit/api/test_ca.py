import json

import pytest

from discovery import api


def ca_roots_response():
    return {
        "ActiveRootID": "c7:bd:55:4b:64:80:14:51:10:a4:b9:b9:d7:e0:75:3f:86:ba:bb:24",
        "TrustDomain": "7f42f496-fbc7-8692-05ed-334aa5340c1e.consul",
        "Roots": [
            {
                "ID": "c7:bd:55:4b:64:80:14:51:10:a4:b9:b9:d7:e0:75:3f:86:ba:bb:24",
                "Name": "Consul CA Root Cert",
                "SerialNumber": 7,
                "SigningKeyID": "2d:09:5d:84:b9:89:4b:dd:e3:88:bb:9c:e2:b2:69:81:1f:4b:a6:fd:4d:df:ee:74:63:f3:74:55:ca:b0:b5:65",
                "ExternalTrustDomain": "a1499528-fbf6-df7b-05e5-ae81e1873fc4",
                "NotBefore": "2018-05-25T21:39:23Z",
                "NotAfter": "2028-05-22T21:39:23Z",
                "RootCert": "-----BEGIN CERTIFICATE-----\nMIICmDCCAj6gAwIBAgIBBzAKBggqhkjOPQQDAjAWMRQwEgYDVQQDEwtDb25zdWwg\nQ0EgNzAeFw0xODA1MjUyMTM5MjNaFw0yODA1MjIyMTM5MjNaMBYxFDASBgNVBAMT\nC0NvbnN1bCBDQSA3MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEq4S32Pu0/VL4\nG75gvdyQuAhqMZFsfBRwD3pgvblgZMeJc9KDosxnPR+W34NXtMD/860NNVJIILln\n9lLhIjWPQqOCAXswggF3MA4GA1UdDwEB/wQEAwIBhjAPBgNVHRMBAf8EBTADAQH/\nMGgGA1UdDgRhBF8yZDowOTo1ZDo4NDpiOTo4OTo0YjpkZDplMzo4ODpiYjo5Yzpl\nMjpiMjo2OTo4MToxZjo0YjphNjpmZDo0ZDpkZjplZTo3NDo2MzpmMzo3NDo1NTpj\nYTpiMDpiNTo2NTBqBgNVHSMEYzBhgF8yZDowOTo1ZDo4NDpiOTo4OTo0YjpkZDpl\nMzo4ODpiYjo5YzplMjpiMjo2OTo4MToxZjo0YjphNjpmZDo0ZDpkZjplZTo3NDo2\nMzpmMzo3NDo1NTpjYTpiMDpiNTo2NTA/BgNVHREEODA2hjRzcGlmZmU6Ly83ZjQy\nZjQ5Ni1mYmM3LTg2OTItMDVlZC0zMzRhYTUzNDBjMWUuY29uc3VsMD0GA1UdHgEB\n/wQzMDGgLzAtgis3ZjQyZjQ5Ni1mYmM3LTg2OTItMDVlZC0zMzRhYTUzNDBjMWUu\nY29uc3VsMAoGCCqGSM49BAMCA0gAMEUCIBBBDOWXWApx4S6bHJ49AW87Nw8uQ/gJ\nJ6lvm3HzEQw2AiEA4PVqWt+z8fsQht0cACM42kghL97SgDSf8rgCqfLYMng=\n-----END CERTIFICATE-----\n",
                "IntermediateCerts": None,
                "Active": True,
                "PrivateKeyType": "ec",
                "PrivateKeyBits": 256,
                "CreateIndex": 8,
                "ModifyIndex": 8,
            }
        ],
    }


def ca_configuration_response():
    return {
        "Provider": "consul",
        "Config": {
            "LeafCertTTL": "72h",
            "RotationPeriod": "2160h",
            "IntermediateCertTTL": "8760h",
        },
        "CreateIndex": 5,
        "ModifyIndex": 5,
    }


def update_payload():
    return json.dumps(
        {
            "Provider": "consul",
            "Config": {
                "LeafCertTTL": "72h",
                "PrivateKey": "-----BEGIN RSA PRIVATE KEY-----...",
                "RootCert": "-----BEGIN CERTIFICATE-----...",
                "RotationPeriod": "2160h",
            },
        }
    )


@pytest.fixture
async def ca(consul_api):
    return api.CA(client=consul_api)


@pytest.mark.parametrize("expected", [ca_roots_response()])
async def test_list_root_certificates(ca, expected):
    ca.client.expected = expected
    response = await ca.list_root_certificates()
    assert response == ca_roots_response()


@pytest.mark.parametrize("expected", [ca_configuration_response()])
async def test_configuration(ca, expected):
    ca.client.expected = expected
    response = await ca.configuration()
    assert response == ca_configuration_response()


async def test_update_configuration(ca, mocker):
    spy = mocker.spy(ca.client, "put")
    await ca.update_configuration(
        "consul",
        {
            "LeafCertTTL": "72h",
            "PrivateKey": "-----BEGIN RSA PRIVATE KEY-----...",
            "RootCert": "-----BEGIN CERTIFICATE-----...",
            "IntermediateCertTTL": "8760h",
        },
    )
    spy.assert_called_with(
        "/v1/connect/ca/configuration",
        json={
            "Provider": "consul",
            "Config": {
                "LeafCertTTL": "72h",
                "PrivateKey": "-----BEGIN RSA PRIVATE KEY-----...",
                "RootCert": "-----BEGIN CERTIFICATE-----...",
                "IntermediateCertTTL": "8760h",
            },
        },
    )
