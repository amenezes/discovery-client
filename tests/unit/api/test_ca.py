import json
import unittest

from discovery.api.ca import CA
from discovery.core.engine.standard import StandardEngine


class TestCA(unittest.TestCase):

    def setUp(self):
        client = StandardEngine()
        self.ca = CA(client)

    def test_list(self):
        self.assertIsNotNone(self.ca.list())

    def test_configuration(self):
        self.assertIsNotNone(self.ca.configuration())

    def test_update(self):
        sample_payload = {
            'Provider': 'consul',
            'Config': {
                'LeafCertTTL': '72h',
                "PrivateKey": '-----BEGIN RSA PRIVATE KEY-----...',
                'RootCert': '-----BEGIN CERTIFICATE-----...',
                'RotationPeriod': '2160h'
            }
        }
        self.assertIsNotNone(self.ca.update(json.dumps(sample_payload)))
