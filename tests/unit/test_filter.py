import unittest

from discovery.filter import Filter


class TestFilter(unittest.TestCase):
    def test_consul_catalog_enum_values(self):
        self.assertEqual(Filter.FIRST_ITEM.value, 0)
        self.assertEqual(Filter.PAYLOAD.value, 1)
