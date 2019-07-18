"""Test Check module."""

import unittest

from discovery.check import (
    Check,
    alias,
    http,
    tcp,
)


class TestCheck(unittest.TestCase):
    """Unit tests to consul's check module."""

    def setUp(self):
        """Mock of responses expected."""
        self.check_tcp = {
            'id': '37a3e86014064d34a7eecb5d56bf8d41',
            'name': 'tcp-check',
            'tcp': 'test:5000',
            'interval': '10s',
            'timeout': '5s'
        }
        self.check_http = {
            'id': '37a3e86014064d34a7eecb5d56bf8d42',
            'name': 'http-check',
            'http': 'http://test:5000/manage/health',
            'interval': '10s',
            'timeout': '5s'
        }
        self.check_alias = {
            'id': '37a3e86014064d34a7eecb5d56bf8d43',
            'alias_service': 'consul'
        }
        self.regexp_id = r'([\w]{32})'

    def test_check_tcp(self):
        """Tests the creation of a new service."""
        check = Check('tcp-check', tcp('test:5000'))

        self.assertEqual(check.name, self.check_tcp['name'])
        self.assertRegex(check.identifier, self.regexp_id)

    def test_check_http(self):
        """Tests the creation of a new service."""
        check = Check('http-check', http('http://test:5000/manage/health'))

        self.assertEqual(check.name, self.check_http['name'])
        self.assertRegex(check.identifier, self.regexp_id)

    def test_check_alias(self):
        """Tests the creation of a new service."""
        check = Check('alias-check', alias('consul'))

        self.assertEqual(check.name, 'alias-check')
        self.assertRegex(check.identifier, self.regexp_id)

    def test_value_property(self):
        """Tests retrieve check object representation."""
        check = Check('str test', alias('alias-test'))

        self.assertIsInstance(check.value, dict)
        self.assertNotEqual(check.value, {})
