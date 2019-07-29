import json
import unittest

from discovery.api.keyring import Keyring
from discovery.core.engine.standard import StandardEngine


class TestKeyring(unittest.TestCase):

    def get_sample_payload(self):
        sample_payload = {'Key': '3lg9DxVfKNzI8O+IQ5Ek+Q=='}
        return json.dumps(sample_payload)

    def setUp(self):
        client = StandardEngine()
        self.keyring = Keyring(client)

    def test_list(self):
        self.assertIsNotNone(self.keyring.list())

    def test_add(self):
        self.assertIsNotNone(
            self.keyring.add(self.get_sample_payload())
        )

    def test_change(self):
        self.assertIsNotNone(
            self.keyring.change(self.get_sample_payload())
        )

    def test_delete(self):
        self.assertIsNotNone(
            self.keyring.delete(self.get_sample_payload())
        )
