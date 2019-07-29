import unittest

from discovery.api.checks import Checks
from discovery.check import Check, alias
from discovery.core.engine.standard import StandardEngine


class TestChecks(unittest.TestCase):

    def setUp(self):
        client = StandardEngine()
        self.checks = Checks(client)
        self.data = Check(alias('consul'), 'test-check')

    def test_checks(self):
        response = self.checks.checks()
        self.assertIsInstance(response.json(), dict)

    def test_register(self):
        response = self.checks.register(self.data.json())
        self.assertIsNotNone(response)

    def test_deregister(self):
        response = self.checks.deregister(self.data.identifier)
        self.assertIsNotNone(response)

    def test_check_pass(self):
        response = self.checks.check_pass(self.data.identifier)
        self.assertIsNotNone(response)

    def test_check_warn(self):
        response = self.checks.check_warn(self.data.identifier)
        self.assertIsNotNone(response)

    def test_check_fail(self):
        response = self.checks.check_fail(self.data.identifier)
        self.assertIsNotNone(response)

    def test_check_update_success(self):
        response = self.checks.check_update(self.data.identifier, 'passing')
        self.assertIsNotNone(response)

    def test_check_update_invalid_type(self):
        with self.assertRaises(TypeError):
            self.checks.check_update(self.data.identifier, 1)

    def test_check_update_value_error(self):
        with self.assertRaises(ValueError):
            self.checks.check_update(self.data.identifier, 'ok')
