import json
import unittest

from discovery.api.service import Service
from discovery.core.engine.standard import StandardEngine


class TestService(unittest.TestCase):

    def get_sample_payload(self):
        return json.dumps({
            'ID': 'redis1',
            'Name': 'redis',
            'Tags': [
                'primary',
                'v1'
            ],
            'Address': '127.0.0.1',
            'Port': 8000,
            'Meta': {
                'redis_version': '4.0'
            },
            'EnableTagOverride': False,
            'Check': {
                'DeregisterCriticalServiceAfter': '90m',
                'HTTP': 'http://localhost:5000/health',
                'Interval': '10s'
            },
            'Weights': {
                'Passing': 10,
                'Warning': 1
            }
        })

    def get_service_id(self):
        response = json.loads(self.get_sample_payload())
        return response.get('ID')

    def get_service_name(self):
        response = json.loads(self.get_sample_payload())
        return response.get('Name')

    def setUp(self):
        client = StandardEngine()
        self.service = Service(client)
        self.service.register(self.get_sample_payload())

    def tearDown(self):
        self.service.deregister(self.get_service_id())

    def test_services(self):
        response = self.service.services()
        self.assertTrue(response.ok)

    def test_service(self):
        response = self.service.service(self.get_service_id())
        self.assertTrue(response.ok)

    def test_configuration(self):
        response = self.service.configuration(self.get_service_id())
        self.assertTrue(response.ok)

    def test_register(self):
        self.service.deregister(self.get_service_id())
        response = self.service.register(self.get_sample_payload())
        self.assertTrue(response.ok)

    def test_deregister(self):
        response = self.service.deregister(self.get_service_id())
        self.assertTrue(response.ok)

    def test_maintenance(self):
        response = self.service.maintenance(
            self.get_service_id(),
            True,
            'For the tests'
        )
        self.assertEqual(response.text, '')
        self.assertTrue(response.ok)

    def test_get_local_service_health(self):
        response = self.service.get_local_service_health(
            self.get_service_name()
        )
        self.assertEqual(response.status_code, 503)

    def test_format_is_valid(self):
        with self.assertRaises(ValueError):
            self.service.get_local_service_health(
                self.get_service_name(),
                ''
            )

    def test_describe_health_code_valid(self):
        response = self.service.get_local_service_health(
            self.get_service_name()
        )
        description = self.service.describe_health_code(
            response.status_code
        )
        self.assertIsInstance(description, str)

    def test_describe_health_code_invalid(self):
        description = self.service.describe_health_code(201)
        self.assertEqual(
            description,
            'Invalid code. Please see: '
            'https://www.consul.io/'
            'api/agent/service.html#get-local-service-health'
        )

    def test_get_local_service_health_by_id(self):
        response = self.service.get_local_service_health_by_id(
            self.get_service_id()
        )
        self.assertEqual(response.status_code, 503)
