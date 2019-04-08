"""Test filter enum."""
import unittest

from discovery.consul.filter import Filter


class TestFilter(unittest.TestCase):
    """Unit tests to filter enum."""

    def test_consul_catalog_enum_values(self):
        """Tests the enum values from consul's catalog."""
        self.assertEqual(Filter.FIRST_ITEM.value, 0)
        self.assertEqual(Filter.PAYLOAD.value, 1)

    def test_default_timeout_enum_value(self):
        """Tests the default value for reconnect timeout."""
        self.assertEqual(Filter.DEFAULT_TIMEOUT.value, 30)


if __name__ == '__main__':
    unittest.main()
