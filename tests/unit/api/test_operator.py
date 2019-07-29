import unittest

from discovery.api.operator import Operator
from discovery.core.engine.standard import StandardEngine


class TestStatus(unittest.TestCase):

    def setUp(self):
        self.client = StandardEngine()

    def test_create_operator(self):
        Operator(self.client)
