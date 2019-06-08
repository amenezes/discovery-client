"""Test service enum."""
import socket
import unittest
import uuid

from discovery import service
from discovery.check import Check, http


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

    def test_default_service_instance(self):
        """Tests the creation of a new service."""
        check = Check('myapp-check', http('http://myapp:5000/manage/health'))
        svc = service.Service('myapp', 5000, check)

        self.assertEqual(svc.name, self.service_model['name'])
        self.assertEqual(svc.port, self.service_model['port'])
        self.assertEqual(svc.ip, self.service_model['ip'])
        # self.assertRegex(svc.id, self.regexp_id)
        # self.assertEqual(svc.healthcheck, self.service_model['healthcheck'])


if __name__ == '__main__':
    unittest.main()
