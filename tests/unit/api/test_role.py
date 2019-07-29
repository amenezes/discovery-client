import json
import unittest

from discovery.api.role import Role
from discovery.core.engine.standard import StandardEngine


class TestRole(unittest.TestCase):

    def get_sample_payload(self):
        return json.dumps({
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
        })

    def setUp(self):
        client = StandardEngine()
        self.role = Role(client)

    def test_create(self):
        response = self.role.create(self.get_sample_payload())
        self.assertIsNotNone(response)
        # self.assertEqual(response, '')

    def test_read(self):
        pass

    def test_read_by_name(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass

    def test_list(self):
        response = self.role.list()
        self.assertIsNotNone(response)
        # self.assertIsInstance(response, list)
