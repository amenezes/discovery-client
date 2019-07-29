import json
import unittest

from discovery.api.connect import Connect
from discovery.core.engine.standard import StandardEngine


class TestConnect(unittest.TestCase):

    def get_sample_payload(self):
        return json.dumps({
            'Target': 'db',
            'ClientCertURI': 'spiffe://dc1-7e567ac2-551d-463f-8497-f78972856fc1.consul/ns/default/dc/dc1/svc/web',
            'ClientCertSerial': '04:00:00:00:00:01:15:4b:5a:c3:94'
        })

    def setUp(self):
        client = StandardEngine()
        self.connect = Connect(client)

    def test_authorize(self):
        response = self.connect.authorize(self.get_sample_payload())
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    def test_ca_roots(self):
        response = self.connect.ca_roots()
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    def test_ca_leaf(self):
        response = self.connect.ca_leaf('web')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    def test_ca_proxy(self):
        response = self.connect.proxy('web-proxy')
        self.assertIsNotNone(response)
        self.assertLogs(level='WARN')
