import json
import unittest
from unittest.mock import MagicMock, patch

from discovery.api.token import Token
from discovery.core.engine.standard import StandardEngine


class TestToken(unittest.TestCase):

    def get_sample_list_response(self):
        return [
            {
                'ID': '5e52a099-4c90-c067-5478-980f06be9af5',
                'Name': 'node-read',
                'Description': '',
                'Policies': [
                    {
                        'ID': '783beef3-783f-f41f-7422-7087dc272765',
                        'Name': 'node-read'
                    }
                ],
                'Hash': 'K6AbfofgiZ1BEaKORBloZf7WPdg45J/PipHxQiBlK1U=',
                'CreateIndex': 50,
                'ModifyIndex': 50
            },
            {
                'ID': 'aa770e5b-8b0b-7fcf-e5a1-8535fcc388b4',
                'Name': 'example-role',
                'Description': 'Showcases all input parameters',
                'Policies': [
                    {
                        'ID': '783beef3-783f-f41f-7422-7087dc272765',
                        'Name': 'node-read'
                    }
                ],
                'ServiceIdentities': [
                    {
                        'ServiceName': 'web'
                    },
                    {
                        'ServiceName': 'db',
                        'Datacenters': [
                            'dc1'
                        ]
                    }
                ],
                'Hash': 'mBWMIeX9zyUTdDMq8vWB0iYod+mKBArJoAhj6oPz3BI=',
                'CreateIndex': 57,
                'ModifyIndex': 57
            }
        ]

    def get_sample_put_response(self):
        return {
            'ID': '8bec74a4-5ced-45ed-9c9d-bca6153490bb',
            'Name': 'example-two',
            'Policies': [
                {
                    'ID': '783beef3-783f-f41f-7422-7087dc272765',
                    'Name': 'node-read'
                }
            ],
            'ServiceIdentities': [
                {
                    'ServiceName': 'db'
                }
            ],
            'Hash': 'OtZUUKhInTLEqTPfNSSOYbRiSBKm3c4vI2p6MxZnGWc=',
            'CreateIndex': 14,
            'ModifyIndex': 28
        }

    def get_sample_payload(self):
        return json.dumps({
            'ID': '8bec74a4-5ced-45ed-9c9d-bca6153490bb',
            'Name': 'example-two',
            'Policies': [
                {
                    'Name': 'node-read'
                }
            ],
            'ServiceIdentities': [
                {
                    'ServiceName': 'db'
                }
            ]
        })

    @patch('discovery.core.engine.standard.requests.Session')
    def setUp(self, RequestsMock):
        self.session = RequestsMock()
        self.session.get = MagicMock(return_value=self.get_sample_put_response())
        self.session.put = MagicMock(return_value=self.get_sample_put_response())
        self.session.delete = MagicMock(return_value=True)
        client = StandardEngine(session=self.session)
        self.token = Token(client)

    def test_create(self):
        response = self.token.create(self.get_sample_payload())
        self.assertIsInstance(response, dict)

    def test_read_by_id(self):
        response = self.token.read_by_id('8bec74a4-5ced-45ed-9c9d-bca6153490bb')
        self.assertIsInstance(response, dict)

    def test_read_by_name(self):
        response = self.token.read_by_name('example-two')
        self.assertIsInstance(response, dict)

    def test_update(self):
        response = self.token.update(
            '8f246b77-f3e1-ff88-5b48-8ec93abf3e05',
            self.get_sample_payload()
        )
        self.assertIsInstance(response, dict)

    def test_delete(self):
        response = self.token.delete('8f246b77-f3e1-ff88-5b48-8ec93abf3e05')
        self.assertTrue(response)

    def test_list(self):
        self.session.get = MagicMock(return_value=self.get_sample_list_response())
        response = self.token.list()
        self.assertIsInstance(response, list)
