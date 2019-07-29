import json
import unittest
from unittest.mock import MagicMock, patch

from discovery.api.license import License
from discovery.core.engine.standard import StandardEngine


class TestLicense(unittest.TestCase):

    def get_sample_payload(self):
        return json.dumps({
            'Valid': True,
            'License': {
                'license_id': '2afbf681-0d1a-0649-cb6c-333ec9f0989c',
                'customer_id': '0259271d-8ffc-e85e-0830-c0822c1f5f2b',
                'installation_id': '*',
                'issue_time': '2018-05-21T20:03:35.911567355Z',
                'start_time': '2018-05-21T04:00:00Z',
                'expiration_time': '2019-05-22T03:59:59.999Z',
                'product': 'consul',
                'flags': {
                    'package': 'premium'
                },
                'features': [
                    'Automated Backups',
                    'Automated Upgrades',
                    'Enhanced Read Scalability',
                    'Network Segments',
                    'Redundancy Zone',
                    'Advanced Network Federation'
                ],
                'temporary': False
            },
            'Warnings': []
        })

    @patch('discovery.core.engine.standard.requests.Session')
    def setUp(self, RequestsMock):
        session = RequestsMock()
        session.get = MagicMock(return_value=self.get_sample_payload())
        session.put = MagicMock(return_value=self.get_sample_payload())
        session.delete = MagicMock(return_value=self.get_sample_payload())
        client = StandardEngine(session=session)
        self.license = License(client=client)

    def test_current(self):
        response = self.license.current()
        self.assertEqual(response, self.get_sample_payload())

    def test_update(self):
        response = self.license.update(data=self.get_sample_payload())
        self.assertEqual(response, self.get_sample_payload())

    def test_reset(self):
        response = self.license.reset()
        self.assertEqual(response, self.get_sample_payload())
