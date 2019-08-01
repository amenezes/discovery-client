import unittest
from unittest.mock import MagicMock, patch

from discovery.api.policy import Policy
from discovery.core.engine.standard import StandardEngine


class TestPolicy(unittest.TestCase):

    def get_sample_payload(self):
        return {
            'Name': 'node-read',
            'Description': 'Grants read access to all node information',
            'Rules': 'node_prefix \'\' { policy = \'read\'}',
            'Datacenters': ['dc1']
        }

    def get_policy_id(self):
        response = self.get_sample_response()
        return response.get('ID')

    def get_sample_response(self):
        return {
            'ID': 'e359bd81-baca-903e-7e64-1ccd9fdc78f5',
            'Name': 'node-read',
            'Description': 'Grants read access to all node information',
            'Rules': 'node_prefix \'\' { policy = \'read\'}',
            'Datacenters': [
                'dc1'
            ],
            'Hash': 'OtZUUKhInTLEqTPfNSSOYbRiSBKm3c4vI2p6MxZnGWc=',
            'CreateIndex': 14,
            'ModifyIndex': 14
        }

    def get_sample_list_response(self):
        return [
            {
                'CreateIndex': 4,
                'Datacenters': None,
                'Description': 'Builtin Policy that grants unlimited access',
                'Hash': 'swIQt6up+s0cV4kePfJ2aRdKCLaQyykF4Hl1Nfdeumk=',
                'ID': '00000000-0000-0000-0000-000000000001',
                'ModifyIndex': 4,
                'Name': 'global-management'
            },
            {
                'CreateIndex': 14,
                'Datacenters': [
                    'dc1'
                ],
                'Description': 'Grants read access to all node information',
                'Hash': 'OtZUUKhInTLEqTPfNSSOYbRiSBKm3c4vI2p6MxZnGWc=',
                'ID': 'e359bd81-baca-903e-7e64-1ccd9fdc78f5',
                'ModifyIndex': 14,
                'Name': 'node-read'
            }
        ]

    @patch('discovery.core.engine.standard.requests.Session')
    def setUp(self, RequestsMock):
        self.session = RequestsMock()
        self.session.get = MagicMock(return_value=self.get_sample_response())
        self.session.put = MagicMock(return_value=self.get_sample_response())
        self.session.delete = MagicMock(return_value=True)
        client = StandardEngine(session=self.session)
        self.policy = Policy(client)

    def test_create(self):
        response = self.policy.create(self.get_sample_payload())
        self.assertIsInstance(response, dict)

    def test_read(self):
        response = self.policy.read(self.get_policy_id())
        self.assertIsInstance(response, dict)

    def test_update(self):
        response = self.policy.update(
            self.get_policy_id(),
            self.get_sample_payload()
        )
        self.assertIsInstance(response, dict)

    def test_delete(self):
        response = self.policy.delete(
            self.get_policy_id()
        )
        self.assertTrue(response)

    def test_list(self):
        self.session.get = MagicMock(
            return_value=self.get_sample_list_response()
        )
        response = self.policy.list()
        self.assertIsInstance(response, list)
