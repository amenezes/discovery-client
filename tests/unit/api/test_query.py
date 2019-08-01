import unittest
from unittest.mock import MagicMock, patch

from discovery.api.query import Query
from discovery.core.engine.standard import StandardEngine


class TestQuery(unittest.TestCase):

    def get_sample_payload(self):
        return {
            'Name': 'my-query',
            'Session': 'adf4238a-882b-9ddc-4a9d-5b6758e4159e',
            'Token': '',
            'Service': {
                'Service': 'redis',
                'Failover': {
                    'NearestN': 3,
                    'Datacenters': ['dc1', 'dc2']
                },
                'Near': 'node1',
                'OnlyPassing': False,
                'Tags': ['primary', '!experimental'],
                'NodeMeta': {'instance_type': 'm3.large'},
                'ServiceMeta': {'environment': 'production'}
            },
            'DNS': {
                'TTL': '10s'
            }
        }

    def get_sample_response(self):
        return {
            'ID': '8f246b77-f3e1-ff88-5b48-8ec93abf3e05'
        }

    def get_sample_read_response(self):
        return [
            {
                'ID': '8f246b77-f3e1-ff88-5b48-8ec93abf3e05',
                'Name': 'my-query',
                'Session': 'adf4238a-882b-9ddc-4a9d-5b6758e4159e',
                'Token': '<hidden>',
                'Service': {
                    'Service': 'redis',
                    'Failover': {
                        'NearestN': 3,
                        'Datacenters': ['dc1', 'dc2']
                    },
                    'OnlyPassing': False,
                    'Tags': ['primary', '!experimental'],
                    'NodeMeta': {'instance_type': 'm3.large'},
                    'ServiceMeta': {'environment': 'production'}
                },
                'DNS': {
                    'TTL': '10s'
                },
                'RaftIndex': {
                    'CreateIndex': 23,
                    'ModifyIndex': 42
                }
            }
        ]

    def get_sample_execute_response(self):
        return {
            'Service': 'redis',
            'Nodes': [
                {
                    'Node': {
                        'ID': '40e4a748-2192-161a-0510-9bf59fe950b5',
                        'Node': 'foobar',
                        'Address': '10.1.10.12',
                        'Datacenter': 'dc1',
                        'TaggedAddresses': {
                            'lan': '10.1.10.12',
                            'wan': '10.1.10.12'
                        },
                        'NodeMeta': {'instance_type': 'm3.large'}
                    },
                    'Service': {
                        'ID': 'redis',
                        'Service': 'redis',
                        'Tags': None,
                        'Meta': {'redis_version': '4.0'},
                        'Port': 8000
                    },
                    'Checks': [
                        {
                            'Node': 'foobar',
                            'CheckID': 'service:redis',
                            'Name': 'Service \'redis\' check',
                            'Status': 'passing',
                            'Notes': '',
                            'Output': '',
                            'ServiceID': 'redis',
                            'ServiceName': 'redis'
                        },
                        {
                            'Node': 'foobar',
                            'CheckID': 'serfHealth',
                            'Name': 'Serf Health Status',
                            'Status': 'passing',
                            'Notes': '',
                            'Output': '',
                            'ServiceID': '',
                            'ServiceName': ''
                        }
                    ],
                    'DNS': {
                        'TTL': '10s'
                    },
                    'Datacenter': 'dc3',
                    'Failovers': 2
                }
            ]
        }

    def get_sample_explain_response(self):
        return {
            'Query': {
                'ID': '8f246b77-f3e1-ff88-5b48-8ec93abf3e05',
                'Name': 'my-query',
                'Session': 'adf4238a-882b-9ddc-4a9d-5b6758e4159e',
                'Token': '<hidden>',
                # 'Name': 'geo-db',
                'Template': {
                    'Type': 'name_prefix_match',
                    'Regexp': '^geo-db-(.*?)-([^\\-]+?)$'
                },
                'Service': {
                    'Service': 'mysql-customer',
                    'Failover': {
                        'NearestN': 3,
                        'Datacenters': ['dc1', 'dc2']
                    },
                    'OnlyPassing': True,
                    'Tags': ['primary'],
                    'Meta': {
                        'mysql_version': '5.7.20'
                    },
                    'NodeMeta': {'instance_type': 'm3.large'}
                }
            }
        }

    def get_id(self):
        response = self.get_sample_response()
        return response.get('ID')

    @patch('discovery.core.engine.standard.requests.Session')
    def setUp(self, RequestsMock):
        self.session = RequestsMock()
        self.session.get = MagicMock(return_value=self.get_sample_read_response())
        self.session.post = MagicMock(return_value=self.get_sample_response())
        self.session.put = MagicMock(return_value=self.get_sample_response())
        self.session.delete = MagicMock(return_value=True)
        client = StandardEngine(session=self.session)
        self.query = Query(client)

    def test_create(self):
        response = self.query.create(self.get_sample_payload())
        self.assertIsInstance(response, dict)

    def test_read_without_uuid(self):
        response = self.query.read()
        self.assertIsInstance(response, list)

    def test_read_with_uuid(self):
        response = self.query.read(self.get_id())
        self.assertIsInstance(response, list)

    def test_delete(self):
        response = self.query.delete(self.get_id())
        self.assertTrue(response)

    def test_update(self):
        response = self.query.update(
            self.get_id(),
            self.get_sample_payload()
        )
        self.assertIsInstance(response, dict)

    def test_execute(self):
        self.session.get = MagicMock(
            return_value=self.get_sample_execute_response()
        )
        response = self.query.execute(self.get_id())
        self.assertIsInstance(response, dict)

    def test_explain(self):
        self.session.get = MagicMock(
            return_value=self.get_sample_explain_response()
        )
        response = self.query.explain(self.get_id())
        self.assertIsInstance(response, dict)
