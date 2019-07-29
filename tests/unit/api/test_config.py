import unittest

from discovery.api.config import Config
from discovery.core.engine.standard import StandardEngine


class TestConfig(unittest.TestCase):

    def get_sample_payload(self):
        return {
            'Kind': 'service-defaults',
            'Name': 'web',
            'Protocol': 'http',
        }

    def setUp(self):
        client = StandardEngine()
        self.config = Config(client)

    def test_apply(self):
        response = self.config.apply(self.get_sample_payload())
        self.assertIsNotNone(response, str)

    def test_get_success(self):
        response = self.config.get('service-defaults', 'web')
        self.assertIsNotNone(response)

    def test_get_type_error(self):
        with self.assertRaises(TypeError):
            self.config.get(1, 'web')

    def test_get_value_error(self):
        with self.assertRaises(ValueError):
            self.config.get('service', 'web')

    def test_list_success(self):
        response = self.config.list('service-defaults')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    def test_list_type_error(self):
        with self.assertRaises(TypeError):
            self.config.list(1)

    def test_list_value_error(self):
        with self.assertRaises(ValueError):
            self.config.list('service')

    def test_delete_success(self):
        response = self.config.delete('service-defaults', 'web')
        self.assertIsNotNone(response)

    def test_delete_type_error(self):
        with self.assertRaises(TypeError):
            self.config.delete(1, 'web')

    def test_delete_value_error(self):
        with self.assertRaises(ValueError):
            self.config.delete('service', 'web')
