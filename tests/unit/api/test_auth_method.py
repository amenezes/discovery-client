import json
import unittest

from discovery.api.auth_method import AuthMethod
from discovery.core.engine.standard import StandardEngine


class TestAuthMethod(unittest.TestCase):

    def get_sample_payload(self):
        return json.dumps({
            'Name': 'minikube',
            'Type': 'kubernetes',
            'Description': 'dev minikube cluster',
            'Config': {
                'Host': 'https://192.0.2.42:8443',
                'CACert': '-----BEGIN CERTIFICATE-----\n...-----END CERTIFICATE-----\n',
                'ServiceAccountJWT': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9...'
            }
        })

    def setUp(self):
        client = StandardEngine()
        self.auth_method = AuthMethod(client)

    def test_create(self):
        response = self.auth_method.create(self.get_sample_payload())
        self.assertIsNotNone(response)

    def test_read(self):
        response = self.auth_method.read('minikube')
        self.assertIsNotNone(response)

    def test_update(self):
        response = self.auth_method.update(
            'minikube',
            self.get_sample_payload()
        )
        self.assertIsNotNone(response)

    def test_delete(self):
        response = self.auth_method.delete('minikube')
        self.assertIsNotNone(response)

    def test_list(self):
        response = self.auth_method.list()
        self.assertIsNotNone(response)
