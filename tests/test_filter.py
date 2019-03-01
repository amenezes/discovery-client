"""Test filter enum."""
import unittest

from discovery.filter import Filter


class TestFilter(unittest.TestCase):
    """Unit tests to filter enum."""

    def test_select_one_randomly(self):
        """Tests the enum values."""
        self.assertEqual(Filter.FIRST_ITEM.value, 0)
        self.assertEqual(Filter.PAYLOAD.value, 1)


if __name__ == '__main__':
    unittest.main()
