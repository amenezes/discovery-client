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

        self.assertEqual(select_one_rr(servicesA), 'a')
        self.assertEqual(select_one_rr(servicesA), 'b')
        self.assertEqual(select_one_rr(servicesA), 'c')
        self.assertEqual(select_one_rr(servicesA), 'a')
        self.assertEqual(select_one_rr(servicesA), 'b')

        # group 2: select alternate services
        servicesB = ['d', 'e']
        servicesC = ['f', 'g', 'h']

        self.assertEqual(select_one_rr(servicesB), 'd')
        self.assertEqual(select_one_rr(servicesC), 'f')
        self.assertEqual(select_one_rr(servicesC), 'g')
        self.assertEqual(select_one_rr(servicesB), 'e')
        self.assertEqual(select_one_rr(servicesB), 'd')
        self.assertEqual(select_one_rr(servicesC), 'h')
        self.assertEqual(select_one_rr(servicesC), 'f')

    def test_select_one_rr_exception(self):
        """Test raise IndexError for empty instances present on consul's catalog."""
        with self.assertRaises(IndexError):
            select_one_rr([])
