import pytest

from discovery import api

authorize_payload = {
    "Target": "db",
    "ClientCertURI": "spiffe://dc1-7e567ac2-551d-463f-8497-f78972856fc1.consul/ns/default/dc/dc1/svc/web",
    "ClientCertSerial": "04:00:00:00:00:01:15:4b:5a:c3:94",
}

authorize_response = {
    "Authorized": True,
    "Reason": "Matched intention: web => db (allow)",
}

ca_roots_response = {
    "ActiveRootID": "15:bf:3a:7d:ff:ea:c1:8c:46:67:6c:db:b8:81:18:36:ad:e5:d0:c7",
    "Roots": [
        {
            "ID": "15:bf:3a:7d:ff:ea:c1:8c:46:67:6c:db:b8:81:18:36:ad:e5:d0:c7",
            "Name": "Consul CA Root Cert",
            "SerialNumber": 7,
            "SigningKeyID": "1f:91:ca:41:8f:ac:67:bf:59:c2:fa:4e:75:5c:d8:f0:55:de:be:75:b8:33:31:d5:24:b0:04:b3:e8:97:5b:7e",
            "ExternalTrustDomain": "a1499528-fbf6-df7b-05e5-ae81e1873fc4",
            "NotBefore": "2018-05-21T16:33:28Z",
            "NotAfter": "2028-05-18T16:33:28Z",
            "RootCert": "-----BEGIN CERTIFICATE-----\nMIICmDCCAj6gAwIBAgIBBzAKBggqhkjOPQQDAjAWMRQwEgYDVQQDEwtDb25zdWwg\nQ0EgNzAeFw0xODA1MjExNjMzMjhaFw0yODA1MTgxNjMzMjhaMBYxFDASBgNVBAMT\nC0NvbnN1bCBDQSA3MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAER0qlxjnRcMEr\niSGlH7G7dYU7lzBEmLUSMZkyBbClmyV8+e8WANemjn+PLnCr40If9cmpr7RnC9Qk\nGTaLnLiF16OCAXswggF3MA4GA1UdDwEB/wQEAwIBhjAPBgNVHRMBAf8EBTADAQH/\nMGgGA1UdDgRhBF8xZjo5MTpjYTo0MTo4ZjphYzo2NzpiZjo1OTpjMjpmYTo0ZTo3\nNTo1YzpkODpmMDo1NTpkZTpiZTo3NTpiODozMzozMTpkNToyNDpiMDowNDpiMzpl\nODo5Nzo1Yjo3ZTBqBgNVHSMEYzBhgF8xZjo5MTpjYTo0MTo4ZjphYzo2NzpiZjo1\nOTpjMjpmYTo0ZTo3NTo1YzpkODpmMDo1NTpkZTpiZTo3NTpiODozMzozMTpkNToy\nNDpiMDowNDpiMzplODo5Nzo1Yjo3ZTA/BgNVHREEODA2hjRzcGlmZmU6Ly8xMjRk\nZjVhMC05ODIwLTc2YzMtOWFhOS02ZjYyMTY0YmExYzIuY29uc3VsMD0GA1UdHgEB\n/wQzMDGgLzAtgisxMjRkZjVhMC05ODIwLTc2YzMtOWFhOS02ZjYyMTY0YmExYzIu\nY29uc3VsMAoGCCqGSM49BAMCA0gAMEUCIQDzkkI7R+0U12a+zq2EQhP/n2mHmta+\nfs2hBxWIELGwTAIgLdO7RRw+z9nnxCIA6kNl//mIQb+PGItespiHZKAz74Q=\n-----END CERTIFICATE-----\n",
            "IntermediateCerts": None,
            "Active": True,
            "PrivateKeyType": "ec",
            "PrivateKeyBits": 256,
            "CreateIndex": 8,
            "ModifyIndex": 8,
        }
    ],
}

leaf_certificate_response = {
    "SerialNumber": "08",
    "CertPEM": "-----BEGIN CERTIFICATE-----\nMIIChjCCAi2gAwIBAgIBCDAKBggqhkjOPQQDAjAWMRQwEgYDVQQDEwtDb25zdWwg\nQ0EgNzAeFw0xODA1MjExNjMzMjhaFw0xODA1MjQxNjMzMjhaMA4xDDAKBgNVBAMT\nA3dlYjBZMBMGByqGSM49AgEGCCqGSM49AwEHA0IABJdLqRKd1SRycFOFceMHOBZK\nQW8HHO8jZ5C8dRswD+IwTd/otJPiaPrVzGOAi4MsaEUgDMemvN1jiywHt3II08mj\nggFyMIIBbjAOBgNVHQ8BAf8EBAMCA7gwHQYDVR0lBBYwFAYIKwYBBQUHAwIGCCsG\nAQUFBwMBMAwGA1UdEwEB/wQCMAAwaAYDVR0OBGEEXzFmOjkxOmNhOjQxOjhmOmFj\nOjY3OmJmOjU5OmMyOmZhOjRlOjc1OjVjOmQ4OmYwOjU1OmRlOmJlOjc1OmI4OjMz\nOjMxOmQ1OjI0OmIwOjA0OmIzOmU4Ojk3OjViOjdlMGoGA1UdIwRjMGGAXzFmOjkx\nOmNhOjQxOjhmOmFjOjY3OmJmOjU5OmMyOmZhOjRlOjc1OjVjOmQ4OmYwOjU1OmRl\nOmJlOjc1OmI4OjMzOjMxOmQ1OjI0OmIwOjA0OmIzOmU4Ojk3OjViOjdlMFkGA1Ud\nEQRSMFCGTnNwaWZmZTovLzExMTExMTExLTIyMjItMzMzMy00NDQ0LTU1NTU1NTU1\nNTU1NS5jb25zdWwvbnMvZGVmYXVsdC9kYy9kYzEvc3ZjL3dlYjAKBggqhkjOPQQD\nAgNHADBEAiBS8kH3UERhBPHM/CQV/jXKLr0kReLqCdq1jZxc8Aq7hQIgFIus/ZX0\nOM/X3Yc1xb/qJiiEVzXcaz3oVFULOzrNAwk=\n-----END CERTIFICATE-----\n",
    "PrivateKeyPEM": "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIAOGglbwY8HdD3LFX6Bc94co2pzeFTto8ebWoML5E+QfoAoGCCqGSM49\nAwEHoUQDQgAEl0upEp3VJHJwU4Vx4wc4FkpBbwcc7yNnkLx1GzAP4jBN3+i0k+Jo\n+tXMY4CLgyxoRSAMx6a83WOLLAe3cgjTyQ==\n-----END EC PRIVATE KEY-----\n",
    "Service": "web",
    "ServiceURI": "spiffe://11111111-2222-3333-4444-555555555555.consul/ns/default/dc/dc1/svc/web",
    "ValidAfter": "2018-05-21T16:33:28Z",
    "ValidBefore": "2018-05-24T16:33:28Z",
    "CreateIndex": 5,
    "ModifyIndex": 5,
}


@pytest.fixture
async def connect(consul_api):
    return api.Connect(client=consul_api)


@pytest.mark.parametrize("expected", [authorize_response])
async def test_authorize(connect, expected):
    connect.client.expected = expected
    response = await connect.authorize(
        "db",
        "spiffe://dc1-7e567ac2-551d-463f-8497-f78972856fc1.consul/ns/default/dc/dc1/svc/web",
        "04:00:00:00:00:01:15:4b:5a:c3:94",
    )
    assert response == authorize_response


@pytest.mark.parametrize("expected", [authorize_response])
async def test_authorize_with_namespace(connect, expected):
    connect.client.expected = expected
    response = await connect.authorize(
        "db",
        "spiffe://dc1-7e567ac2-551d-463f-8497-f78972856fc1.consul/ns/default/dc/dc1/svc/web",
        "04:00:00:00:00:01:15:4b:5a:c3:94",
        "default",
    )
    assert response == authorize_response


@pytest.mark.parametrize("expected", [ca_roots_response])
async def test_ca_roots(connect, expected):
    connect.client.expected = expected
    response = await connect.ca_roots()
    assert response == ca_roots_response


@pytest.mark.parametrize("expected", [leaf_certificate_response])
async def test_leaf_certificate(connect, expected):
    connect.client.expected = expected
    response = await connect.leaf_certificate("web")
    assert response == leaf_certificate_response
