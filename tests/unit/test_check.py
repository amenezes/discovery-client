"""Test Check module."""
import unittest

from discovery.consul.check import Check


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
        self.regexp_tcp = r''
        self.regexp_http = r''
        self.regexp_alias = r'(.id.{4}[\w]{32}.{1,3}.alias_service.{1,4}\w+.)'

    def test_check_tcp(self):
        """Tests the creation of a new service."""
        check = Check('tcp-check')
        check.tcp('test:5000')

        self.assertEqual(check.name, self.check_tcp['name'])
        self.assertRegex(check.id, self.regexp_id)

    def test_check_http(self):
        """Tests the creation of a new service."""
        check = Check('http-check')
        check.http('http://test:5000/manage/health')

        self.assertEqual(check.name, self.check_http['name'])
        self.assertRegex(check.id, self.regexp_id)

    def test_check_alias(self):
        """Tests the creation of a new service."""
        check = Check('alias-check')
        check.alias('consul')

        self.assertEqual(check.name, 'alias-check')
        self.assertRegex(check.id, self.regexp_id)
        self.assertRegex(str(check.value), self.regexp_alias)


if __name__ == '__main__':
    unittest.main()