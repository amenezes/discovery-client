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
        self.check = Check('myapp-check', http('http://myapp:5000/manage/health'))
        self.svc = service.Service('myapp',
                                   5000,
                                   ip=socket.gethostbyname(socket.gethostname()),
                                   check=self.check)

    def test_default_service_instance(self):
        """Tests the creation of a new service."""
        self.assertEqual(self.svc.name, self.service_model['name'])
        self.assertEqual(self.svc.port, self.service_model['port'])
        self.assertEqual(self.svc.ip, self.service_model['ip'])

    def test_set_custom_check(self):
        """Tests the use case to append custom check."""
        custom_svc = service.Service('myapp-without-check', 5001)
        self.assertIsInstance(custom_svc.check, dict)
        self.assertDictEqual(custom_svc.check, {})

    def test_service_str(self):
        """Tests the overwriting of the __str__ magic method."""
        svc = service.Service('myapp', 5000, Check('svc-check', alias('alias-test')))

        regex_str = r'(Service.{17}name.{2}myapp.{2}port.{2}5000.{2}id.{42}ip.{16})'
        self.assertRegex(str(svc), regex_str)

    def test_additional_checks(self):
        """Tests additional check in a service registered."""
        consul_check = Check('consul', alias('consul'))
        self.svc.append(consul_check)

        self.assertEqual(len(self.svc.additional_checks()), 1)

    def test_append_invalid_check(self):
        """Tests if an invalid check will raise TypeError."""
        with self.assertRaises(TypeError):
            self.svc.append(alias('consul'))

    def test_remove_additional_check(self):
        """Tests remove additional check."""
        self.svc.append(Check('consul', alias('consul')))
        self.assertEqual(len(self.svc.additional_checks()), 1)

        self.svc.remove('consul')
        self.assertEqual(len(self.svc.additional_checks()), 0)

    def test_remove_invalid_check(self):
        """Tests if an invalid deregister will raise ValueError."""
        self.svc.append(Check('consul', alias('consul')))
        self.assertEqual(len(self.svc.additional_checks()), 1)

        with self.assertRaises(ValueError):
            self.svc.remove('myapp')

    def test_additional_check(self):
        """Tests if additional check was registered with successfuly."""
        consul_check = Check('consul', alias('consul'))
        self.svc.append(consul_check)

        self.assertIsInstance(self.svc.additional_check('consul'), Check)
        self.assertEqual(self.svc.additional_check('consul').name, 'consul')

    def test_additional_check_invalid(self):
        """Tests if an invalid Check will raise ValueError."""
        consul_check = Check('consul', alias('consul'))
        self.svc.append(consul_check)

        with self.assertRaises(ValueError):
            self.svc.additional_check('teste-consul')
