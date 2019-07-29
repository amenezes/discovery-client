import json
import unittest
from unittest.mock import MagicMock, patch

from discovery.api.area import Area
from discovery.core.engine.standard import StandardEngine


class TestLicense(unittest.TestCase):

    def get_sample_payload(self):
        return json.dumps({
            'PeerDatacenter': 'dc2',
            'RetryJoin': ['10.1.2.3', '10.1.2.4', '10.1.2.5'],
            'UseTLS': False
        })

    def get_area_payload(self):
        return json.dumps(
            [{
                'ID': '8f246b77-f3e1-ff88-5b48-8ec93abf3e05',
                'PeerDatacenter': 'dc2',
                'RetryJoin': ['10.1.2.3', '10.1.2.4', '10.1.2.5']
            }]
        )

    def get_join_payload(self):
        return json.dumps(
            [
                {
                    'Address': '10.1.2.3',
                    'Joined': True,
                    'Error': ''
                },
                {
                    'Address': '10.1.2.4',
                    'Joined': True,
                    'Error': ''
                },
                {
                    'Address': '10.1.2.5',
                    'Joined': True,
                    'Error': ''
                }
            ]
        )

    def get_members_payload(self):
        return json.dumps([
            {
                'ID': 'afc5d95c-1eee-4b46-b85b-0efe4c76dd48',
                'Name': 'node-2.dc1',
                'Addr': '127.0.0.2',
                'Port': 8300,
                'Datacenter': 'dc1',
                'Role': 'server',
                'Build': '0.8.0',
                'Protocol': 2,
                'Status': 'alive',
                'RTT': 256478
            },
        ])

    @patch('discovery.core.engine.standard.requests.Session')
    def setUp(self, RequestsMock):
        self.session = RequestsMock()
        self.session.post = MagicMock(return_value=self.get_sample_payload())
        self.session.get = MagicMock(return_value=self.get_area_payload())
        self.session.put = MagicMock()
        self.session.delete = MagicMock()
        client = StandardEngine(session=self.session)
        self.area = Area(client=client)

    def test_create(self):
        response = self.area.create(self.get_sample_payload())
        self.assertEqual(response, self.get_sample_payload())

    def test_list_without_uuid(self):
        response = self.area.list()
        self.assertEqual(response, self.get_area_payload())

    def test_list_with_uuid(self):
        response = self.area.list('8f246b77-f3e1-ff88-5b48-8ec93abf3e05')
        self.assertEqual(response, self.get_area_payload())

    def test_update(self):
        response = self.area.update(
            '8f246b77-f3e1-ff88-5b48-8ec93abf3e05',
            json.dumps({'UseTLS': True})
        )
        self.assertTrue(response)

    def test_delete(self):
        response = self.area.delete('8f246b77-f3e1-ff88-5b48-8ec93abf3e05')
        self.assertTrue(response)

    def test_join(self):
        self.session.put = MagicMock(return_value=self.get_join_payload())
        response = self.area.join(
            '8f246b77-f3e1-ff88-5b48-8ec93abf3e05',
            json.dumps(['10.1.2.3', '10.1.2.4', '10.1.2.5'])
        )
        self.assertEqual(response, self.get_join_payload())

    def test_members(self):
        self.session.get = MagicMock(return_value=self.get_members_payload())
        response = self.area.members(
            '8f246b77-f3e1-ff88-5b48-8ec93abf3e05'
        )
        self.assertEqual(response, self.get_members_payload())
