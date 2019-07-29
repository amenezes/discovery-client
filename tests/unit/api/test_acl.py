import unittest

from discovery.api.acl import Acl
from discovery.core.engine.standard import StandardEngine


class TestAcl(unittest.TestCase):

    def setUp(self):
        self.client = StandardEngine()

    def test_create_acl(self):
        Acl(self.client)
