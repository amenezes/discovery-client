import json
import unittest

from discovery.api.txn import Txn
from discovery.core.engine.standard import StandardEngine


class TestTxn(unittest.TestCase):

    def get_sample_payload(self):
        return json.dumps([
            {
                'KV': {
                    'Verb': 'get',
                    'Key': '<key>',
                    'Value': '<Base64-encoded blob of data>',
                    'Flags': '<flags>',
                    'Index': '<index>',
                    'Session': '<session id>'
                }
            },
            {
                'Node': {
                    'Verb': 'set',
                    'Node': {
                        'ID': '67539c9d-b948-ba67-edd4-d07a676d6673',
                        'Node': 'bar',
                        'Address': '192.168.0.1',
                        'Datacenter': 'dc1',
                        'Meta': {
                            'instance_type': 'm2.large'
                        }
                    }
                }
            },
            {
                'Service': {
                    'Verb': 'delete',
                    'Node': 'foo',
                    'Service': {
                        'ID': 'db1'
                    }
                }
            },
            {
                'Check': {
                    'Verb': 'cas',
                    'Check': {
                        'Node': 'bar',
                        'CheckID': 'service:web1',
                        'Name': 'Web HTTP Check',
                        'Status': 'critical',
                        'ServiceID': 'web1',
                        'ServiceName': 'web',
                        'ServiceTags': None,
                        'Definition': {
                            'HTTP': 'http://localhost:8080',
                            'Interval': '10s'
                        },
                        'ModifyIndex': 22
                    }
                }
            }
        ])

    def setUp(self):
        client = StandardEngine()
        self.txn = Txn(client)

    def test_create(self):
        response = self.txn.create(self.get_sample_payload())
        self.assertIsNotNone(response)
        # self.assertEqual(response.status_code, 200)
