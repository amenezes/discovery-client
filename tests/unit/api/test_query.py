import json
import unittest

from discovery.api.query import Query
from discovery.api.session import Session
from discovery.core.engine.standard import StandardEngine


class TestQuery(unittest.TestCase):

    _id = None

    def create_session(self):
        payload = {
            'LockDelay': '15s',
            'Name': 'my-service-lock',
            'Node': 'foobar',
            'Checks': ['a', 'b', 'c'],
            'Behavior': 'release',
            'TTL': '30s'
        }
        session = Session(self.client)
        response = session.create(payload)
        return response.json()

    def get_sample_payload(self):
        session = self.create_session()
        return json.dumps({
            'Name': 'my-query',
            'Session': f"{session.get('ID')}",
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
        })

    def create_query(self):
        query_payload = self.get_sample_payload()
        response = self.query.create(query_payload)
        return response.json()

    def setUp(self):
        self.client = StandardEngine()
        self.query = Query(self.client)
        # self._id = self.create_query()

    @unittest.skip
    def tearDown(self):
        self.query.delete(self._id)

    @unittest.skip
    def test_create(self):
        self.assertIsNotNone(self._id)
        self.assertIsInstance(self._id, dict)

    @unittest.skip
    def test_read_without_uuid(self):
        response = self.query.read()
        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)

    @unittest.skip
    def test_read_with_uuid(self):
        response = self.query.read(self._id)
        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)

    @unittest.skip
    def test_update(self):
        response = self.query.update(self._id, 'query_payload')
        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)

    @unittest.skip
    def test_delete(self):
        response = self.query.delete(self._id)
        self.assertIsNone(response)

    @unittest.skip
    def test_execute(self):
        response = self.query.execute(self._id)
        self.assertIsNone(response)

    @unittest.skip
    def test_explain(self):
        response = self.query.explain(self._id)
        self.assertIsNone(response)
