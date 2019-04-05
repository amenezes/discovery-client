"""Test service enum."""
import socket
import unittest
import uuid

from discovery import service


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
                'http': 'http://myapp:5000/manage/health',
                'DeregisterCriticalServiceAfter': '1m',
                'interval': '10s',
                'timeout': '5s'
            }
        }
        self.regexp_id = r'(myapp-.{32})'

    def test_default_service_instance(self):
        """Tests the creation of a new service."""
        svc = service.Service('myapp', 5000)

        self.assertEqual(svc.name, self.service_model['name'])
        self.assertEqual(svc.port, self.service_model['port'])
        self.assertEqual(svc.ip, self.service_model['ip'])
        self.assertRegex(svc.id, self.regexp_id)
        self.assertEqual(svc.healthcheck, self.service_model['healthcheck'])

    def test_healthcheck_setter_error(self):
        """Tests the error raised by healthcheck property logic.."""
        svc = service.Service('myapp', 5000)

        with self.assertRaises(TypeError):
            svc.healthcheck = ''

    def test_healthcheck_setter(self):
        """Tests the setter logic of healthcheck property."""
        svc = service.Service('myapp', 5000)
        custom_healthcheck = {
            'healthcheck': {
                'http': 'http://myapp:5000/manage/health',
                'DeregisterCriticalServiceAfter': '30s',
                'interval': '60s',
                'timeout': '10s'
            }
        }
        svc.healthcheck = custom_healthcheck

        self.assertIsInstance(custom_healthcheck, dict)
        self.assertEqual(svc.healthcheck, custom_healthcheck)


if __name__ == '__main__':
    unittest.main()
