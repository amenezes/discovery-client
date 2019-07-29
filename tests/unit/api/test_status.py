import unittest

from discovery.api.status import Status
from discovery.core.engine.standard import StandardEngine


class TestStatus(unittest.TestCase):

    def setUp(self):
        client = StandardEngine()
        self.status = Status(client)

    def test_leader(self):
        response = self.status.leader()
        self.assertIsNotNone(response)
        self.assertEqual(response.json(), '127.0.0.1:8300')

    def test_peers(self):
        response = self.status.peers()
        self.assertIsNotNone(response)
        self.assertEqual(response.json(), ['127.0.0.1:8300'])
