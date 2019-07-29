import json
import unittest

from discovery.api.kv import Kv
from discovery.core.engine.standard import StandardEngine


class TestKv(unittest.TestCase):

    def get_sample_data(self):
        data = {'key': 'value'}
        return json.dumps(data)

    def setUp(self):
        client = StandardEngine()
        self.kv = Kv(client)

    def test_create(self):
        self.assertTrue(self.kv.create('test_key', self.get_sample_data()))

    def test_read(self):
        self.kv.update('test_key', self.get_sample_data())
        self.assertIsNotNone(self.kv.read('test_key'))

    def test_update(self):
        self.assertTrue(self.kv.update('test_key', self.get_sample_data()))

    def test_delete(self):
        self.kv.update('test_key', self.get_sample_data())
        self.assertTrue(self.kv.delete('test_key'))
