import json
import unittest

from discovery.api.catalog import Catalog
from discovery.core.engine.standard import StandardEngine


class TestCatalog(unittest.TestCase):

    def get_sample_payload(self):
        return json.dumps({
            'Datacenter': 'dc1',
            'ID': '40e4a748-2192-161a-0510-9bf59fe950b5',
            'Node': 'foobar',
            'Address': '192.168.10.10',
            'TaggedAddresses': {
                'lan': '192.168.10.10',
                'wan': '10.0.10.10'
            },
            'NodeMeta': {
                'somekey': 'somevalue'
            },
            'Service': {
                'ID': 'redis1',
                'Service': 'redis',
                'Tags': [
                    'primary',
                    'v1'
                ],
                'Address': '127.0.0.1',
                'TaggedAddresses': {
                    'lan': {
                        'address': '127.0.0.1',
                        'port': 8000
                    },
                    'wan': {
                        'address': '198.18.0.1',
                        'port': 80
                    }
                },
                'Meta': {
                    'redis_version': '4.0'
                },
                'Port': 8000
            },
            'Check': {
                'Node': 'foobar',
                'CheckID': 'service:redis1',
                'Name': 'Redis health check',
                'Notes': 'Script based health check',
                'Status': 'passing',
                'ServiceID': 'redis1',
                'Definition': {
                    'TCP': 'localhost:8888',
                    'Interval': '5s',
                    'Timeout': '1s',
                    'DeregisterCriticalServiceAfter': '30s'
                }
            },
            'SkipNodeUpdate': False
        })

    def setUp(self):
        client = StandardEngine()
        self.catalog = Catalog(client)

    def test_register(self):
        response = self.catalog.register(self.get_sample_payload())
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    def test_deregister(self):
        response = self.catalog.deregister(self.get_sample_payload())
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    def test_datacenters(self):
        self.assertIsNotNone(self.catalog.datacenters())

    def test_nodes(self):
        self.assertIsNotNone(self.catalog.nodes())

    def test_services(self):
        self.assertIsNotNone(self.catalog.services())

    def test_service(self):
        self.assertIsNotNone(self.catalog.service('consul'))

    def test_connect(self):
        self.assertIsNotNone(self.catalog.connect('consul'))

    def test_node(self):
        node = self.catalog.nodes()
        node = node.json()[0].get('Node')
        self.assertIsNotNone(self.catalog.node(node))
