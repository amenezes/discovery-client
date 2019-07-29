import unittest

from discovery.api.raft import Raft
from discovery.core.engine.standard import StandardEngine


class TestRaft(unittest.TestCase):

    def setUp(self):
        client = StandardEngine()
        self.raft = Raft(client)

    def test_read_configuration(self):
        response = self.raft.read_configuration()
        self.assertIsInstance(response.json(), dict)
        self.assertIsNotNone(response)

    def test_delete_peer(self):
        self.raft.delete_peer(dc='dc1', address='127.0.0.1:8300')
