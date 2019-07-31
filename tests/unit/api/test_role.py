import unittest
from unittest.mock import MagicMock, patch

from discovery.api.role import Role
from discovery.core.engine.standard import StandardEngine


class TestRole(unittest.TestCase):

    def get_sample_payload(self):
        return {
            'Name': 'example-role',
            'Description': 'Showcases all input parameters',
            'Policies': [
                {
                    'ID': '783beef3-783f-f41f-7422-7087dc272765'
                },
                {
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
            ]
        }

    def get_sample_response(self):
        return {
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

    def get_role_id(self):
        response = self.get_sample_response()
        return response.get('ID')

    @patch('discovery.core.engine.standard.requests.Session')
    def setUp(self, RequestsMock):
        self.session = RequestsMock()
        self.session.get = MagicMock(return_value=self.get_sample_response())
        self.session.put = MagicMock(return_value=self.get_sample_response())
        self.session.delete = MagicMock(return_value=True)
        client = StandardEngine(session=self.session)
        self.role = Role(client)

    def test_create(self):
        response = self.role.create(self.get_sample_payload())
        self.assertIsInstance(response, dict)

    def test_read_by_id(self):
        response = self.role.read_by_id(self.get_role_id())
        self.assertIsInstance(response, dict)

    def test_read_by_name(self):
        response = self.role.read_by_name('example-role')
        self.assertIsInstance(response, dict)

    def test_update(self):
        response = self.role.update(
            self.get_role_id(),
            self.get_sample_payload()
        )
        self.assertIsInstance(response, dict)

    def test_delete(self):
        response = self.role.delete(self.get_role_id())
        self.assertTrue(response)

    def test_list(self):
        self.session.get = MagicMock(return_value=self.get_sample_list_response())
        response = self.role.list()
        self.assertIsInstance(response, list)
