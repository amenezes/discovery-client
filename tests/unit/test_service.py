"""Test service enum."""

import socket
import unittest
import uuid

from discovery import service
from discovery.check import Check, alias, http


class TestFilter(unittest.TestCase):
    """Unit tests to consul's service module."""

    def setUp(self):
        """Mock of responses expected."""
        self.service_model = {
            'name': 'myapp',
            'port': 5000,
            'id': f"myapp-{uuid.uuid4().hex}",
            'ip': socket.gethostbyname(socket.gethostname()),
            'healthcheck': {
                'id': '37a3e86014064d34a7eecb5d56bf8d43',
                'name': 'myapp-check',
                'http': 'http://myapp:5000/manage/health',
                'interval': '10s',
                'timeout': '5s'
            }
        }
        self.check = Check(
            'myapp-check',
            http('http://myapp:5000/manage/health')
        )
        self.svc = service.Service(
            'myapp',
            5000,
            ip=socket.gethostbyname(socket.gethostname()),
            check=self.check
        )

    def test_create_service_with_check(self):
        """Tests the creation of a new service."""
        self.assertEqual(self.svc.name, self.service_model['name'])
        self.assertEqual(self.svc.port, self.service_model['port'])
        self.assertEqual(self.svc.ip, self.service_model['ip'])

    def test_create_service_without_check(self):
        svc = service.Service('myapp2', 5001)
        self.assertIsNone(svc.check)

    def test_check_property(self):
        """Tests if additional check was registered with successfuly."""
        consul_check = Check('consul', alias('consul'))
        self.svc.check = consul_check

        self.assertIsInstance(self.svc.check, Check)

    def test_check_invalid_property(self):
        """Tests if an invalid check will raise TypeError."""
        with self.assertRaises(TypeError):
            self.svc.check = 'consul'

    def test_raw_output(self):
        self.assertIsInstance(self.svc.raw, dict)

    def test_append(self):
        self.svc.append(Check('test', alias('consul')))
        self.assertIn(self.svc.get_check('test'), self.svc.list_checks())

    def test_invalid_append(self):
        with self.assertRaises(TypeError):
            self.svc.append('check')

    def test_remove(self):
        """Tests remove additional check."""
        chk = Check('test', alias('consul'))
        self.svc.append(chk)
        self.assertIn(chk, self.svc.list_checks())

        self.svc.remove(chk.name)
        self.assertNotIn(chk, self.svc.list_checks())

    def test_remove_app_check(self):
        self.svc.remove(self.check.name)
        self.assertNotIn(self.check.name, self.svc.list_checks())

    def test_invalid_remove(self):
        """Tests if an invalid deregister will raise ValueError."""
        with self.assertRaises(ValueError):
            self.svc.remove('non-exist-check')
    
    def test_get_invalid_check(self):
        with self.assertRaises(ValueError):
            self.svc.get_check('non-exist-check')
