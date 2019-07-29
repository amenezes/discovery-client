import unittest

from discovery.api.snapshot import Snapshot
from discovery.core.engine.standard import StandardEngine


class TestSnapshot(unittest.TestCase):

    def setUp(self):
        client = StandardEngine()
        self.snapshot = Snapshot(client)

    def test_generate(self):
        response = self.snapshot.generate()
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    def test_restore(self):
        snapshot = self.snapshot.generate()
        response = self.snapshot.restore(snapshot)
        self.assertIsNotNone(response)
