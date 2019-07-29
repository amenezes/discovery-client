import unittest

from discovery.api.catalog import Catalog
from discovery.api.session import Session
from discovery.core.engine.standard import StandardEngine


class TestSession(unittest.TestCase):

    def get_sample_payload(self):
        {
            'LockDelay': '15s',
            'Name': 'my-service-lock',
            'Node': 'foobar',
            'Checks': ['a', 'b', 'c'],
            'Behavior': 'release',
            'TTL': '30s'
        }

    def get_node(self):
        catalog = Catalog(self.client)
        node = catalog.nodes()
        return node.json()[0].get('Node')

    def get_session(self):
        response = self.session.create(self.get_sample_payload())
        return response.json()

    def setUp(self):
        self.client = StandardEngine()
        self.session = Session(self.client)

    def test_create(self):
        response = self.get_session()
        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)

    def test_delete(self):
        session = self.get_session()
        response = self.session.delete(session.get('ID'), dc='dc1')
        self.assertTrue(response)

    def test_read(self):
        session = self.get_session()
        response = self.session.read(session.get('ID'))
        self.assertIsNotNone(response)
        self.assertIsInstance(response.json(), list)

    def test_list_node_session(self):
        node = self.get_node()
        response = self.session.list_node_session(node)
        self.assertIsNotNone(response)
        self.assertIsInstance(response.json(), list)

    def test_list(self):
        response = self.session.list()
        self.assertIsNotNone(response)
        self.assertIsInstance(response.json(), list)

    def test_renew(self):
        session = self.get_session()
        response = self.session.renew(session.get('ID'))
        self.assertIsNotNone(response)
        self.assertIsInstance(response.json(), list)
