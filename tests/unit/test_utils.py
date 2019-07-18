"""Test utils module."""

import unittest

from discovery.utils import select_one_random, select_one_rr


class TestUtils(unittest.TestCase):
    """Unit tests to utils module."""

    def test_select_one_random(self):
        """Tests the random selection of an instance in a list."""
        services = ['a', 'b', 'c']

        self.assertIn(select_one_random(services), services)
        self.assertIn(select_one_random(services), services)
        self.assertIn(select_one_random(services), services)

    def test_select_one_rr(self):
        """Tests the round robin return of instances present in a list."""
        # group 1: select single service
        servicesA = ['a', 'b', 'c']

        self.assertEqual('a', select_one_rr(servicesA))
        self.assertEqual('b', select_one_rr(servicesA))
        self.assertEqual('c', select_one_rr(servicesA))
        self.assertEqual('a', select_one_rr(servicesA))

        # group 2: select alternate services
        servicesB = ['d', 'e']
        servicesC = ['f', 'g', 'h']

        self.assertEqual('d', select_one_rr(servicesB))
        self.assertEqual('f', select_one_rr(servicesC))
        self.assertEqual('g', select_one_rr(servicesC))
        self.assertEqual('e', select_one_rr(servicesB))
        self.assertEqual('d', select_one_rr(servicesB))

    @unittest.skip
    def test_select_one_rr_exception(self):
        """Test raise IndexError for empty instances present on consul's catalog."""
        instances = ['a', 'b']

        self.assertEqual('a', select_one_rr(instances))
        with self.assertRaises(IndexError):
            select_one_rr([])
