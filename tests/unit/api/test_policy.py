import json
import unittest

from discovery.api.policy import Policy
from discovery.core.engine.standard import StandardEngine


class TestPolicy(unittest.TestCase):

    def get_sample_payload(self):
        return json.dumps({
            'Name': 'node-read',
            'Description': 'Grants read access to all node information',
            'Rules': 'node_prefix "" { policy = "read"}',
            'Datacenters': ['dc1']
        })

    def get_policy_id(self):
        response = self.policy.list()
        return response.json().get('ID')

    def setUp(self):
        client = StandardEngine()
        self.policy = Policy(client)

    def test_create(self):
        response = self.policy.create(self.get_sample_payload())
        self.assertIsNotNone(response)
        # self.assertEqual(response, '')

    @unittest.skip
    def test_read(self):
        response = self.policy.read(self.get_policy_id())
        self.assertIsNotNone(response)

    @unittest.skip
    def test_update(self):
        response = self.policy.update(self.get_sample_payload())
        self.assertIsNotNone(response)
        self.assertTrue(response.ok)

    @unittest.skip
    def test_delete(self):
        response = self.policy.delete(self.get_policy_id(self.get_policy_id()))
        self.assertTrue(response)

    @unittest.skip
    def test_list(self):
        response = self.policy.list()
        self.assertIsNotNone(response)
        self.assertIsInstance(response.json(), list)
