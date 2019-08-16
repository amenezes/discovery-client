import socket
import unittest
import uuid

from discovery import service
from discovery.check import (
    Check,
    alias,
    docker,
    grpc,
    http,
    script,
    tcp,
    ttl
)


class TestService(unittest.TestCase):
    """Unit tests to consul's service module."""

    def setUp(self):
        """Mock of responses expected."""
        self.service_model = {
            'name': 'myapp',
            'port': 5000,
            'id': f"myapp-{uuid.uuid4().hex}",
            'address': socket.gethostbyname(socket.gethostname()),
            'healthcheck': {
                'id': '37a3e86014064d34a7eecb5d56bf8d43',
                'name': 'myapp-check',
                'http': 'http://myapp:5000/manage/health',
                'interval': '10s',
                'timeout': '5s'
            }
        }
        self.check = Check(
            http('http://myapp:5000/manage/health'),
            'myapp-check'
        )
        self.svc = service.Service(
            name='myapp',
            port=5000,
            address=socket.gethostbyname(socket.gethostname()),
            check=self.check
        )

    def test_create_service_with_check(self):
        """Tests the creation of a new service."""
        self.assertEqual(self.svc.name, self.service_model.get('name'))
        self.assertEqual(self.svc.port, self.service_model.get('port'))
        self.assertEqual(self.svc.address, self.service_model.get('address'))

    def test_create_service_without_check(self):
        svc = service.Service(name='myapp2', port=5001)
        self.assertIsNone(svc.check)

    def test_service_check_property(self):
        """Tests if additional check was registered with successfuly."""
        consul_check = Check(alias('consul'), name='consul')
        self.svc.check = consul_check
        self.assertIsInstance(self.svc.check, Check)

    def test_json(self):
        self.assertIsNotNone(self.svc.json())
        self.assertIsInstance(self.svc.json(), str)

    def test_set_invalid_check(self):
        with self.assertRaises(TypeError):
            self.svc.check = 1

    def test_invalid_append(self):
        with self.assertRaises(TypeError):
            self.svc.append('check')

    def test_get_invalid_check(self):
        with self.assertRaises(ValueError):
            self.svc.get_check('non-exist-check')

    def test_append(self):
        self.svc.append(Check(alias('consul'), 'test'))
        self.assertIn(self.svc.get_check('test'), self.svc.list_checks())

    def test_remove(self):
        """Tests remove additional check."""
        chk = Check(alias('consul'), 'test')
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

    def test_alias_check(self):
        self.assertIsInstance(alias('consul'), dict)

    def test_script_check(self):
        self.assertIsInstance(
            script(["/usr/local/bin/check_mem.py", "-limit", "256MB"]),
            dict
        )

    def test_http_check(self):
        self.assertIsInstance(
            http('http://localhost:5000/manage/health'),
            dict
        )

    def test_tcp_check(self):
        self.assertIsInstance(tcp('localhost:22'), dict)

    def test_ttl_check(self):
        self.assertIsInstance(
            ttl('Web app does a curl internally every 30 seconds', '30s'),
            dict
        )

    def test_docker_check(self):
        self.assertIsInstance(
            docker(container_id='f972c95ebf0e', args=['/usr/local/bin/check_mem.py']),
            dict
        )

    def test_grpc_check(self):
        self.assertIsInstance(grpc('127.0.0.1:12345'), dict)