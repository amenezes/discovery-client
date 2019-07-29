import unittest

from discovery.api.catalog import Catalog
from discovery.api.health import Health
from discovery.core.engine.standard import StandardEngine


class TestHealth(unittest.TestCase):

    def get_node(self):
        catalog = Catalog(self.client)
        node = catalog.nodes()
        return node.json()[0].get('Node')

    def setUp(self):
        self.client = StandardEngine()
        self.health = Health(self.client)

    def test_node(self):
        self.assertIsNotNone(self.health.node(self.get_node()))

    def test_checks(self):
        self.assertIsNotNone(self.health.checks('consul'))

    def test_service(self):
        self.assertIsNotNone(self.health.service('consul'))

    def test_connect(self):
        self.assertIsNotNone(self.health.connect('consul'))

    def test_state_success(self):
        self.assertIsNotNone(self.health.state('passing'))

    def test_state_type_error(self):
        with self.assertRaises(TypeError):
            self.health.state(list)

    def test_state_value_error(self):
        with self.assertRaises(ValueError):
            self.health.state('ok')
