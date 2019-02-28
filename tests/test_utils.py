"""Test utils module."""
import unittest

from discovery.utils import select_one_randomly, select_one_rr


class TestUtils(unittest.TestCase):
    """Unit tests to utils module."""

    def test_select_one_randomly(self):
        """Tests the random selection of an instance in a list."""
        services = ['a', 'b', 'c']

        self.assertIn(select_one_randomly(services), services)

    def test_select_one_rr(self):
        """Tests the round robin return of instances present in a list."""
        # group 1: select single service
        serviceA = 'serviceA'
        servicesA = ['a', 'b', 'c']

        self.assertEqual(select_one_rr(serviceA, servicesA), 'a')
        self.assertEqual(select_one_rr(serviceA, servicesA), 'b')
        self.assertEqual(select_one_rr(serviceA, servicesA), 'c')
        self.assertEqual(select_one_rr(serviceA, servicesA), 'a')

        # group 2: select alternate services
        serviceB = 'serviceB'
        servicesB = ['d', 'e']

        serviceC = 'serviceC'
        servicesC = ['f', 'g', 'h']

        self.assertEqual(select_one_rr(serviceB, servicesB), 'd')
        self.assertEqual(select_one_rr(serviceC, servicesC), 'f')
        self.assertEqual(select_one_rr(serviceC, servicesC), 'g')
        self.assertEqual(select_one_rr(serviceB, servicesB), 'e')
        self.assertEqual(select_one_rr(serviceB, servicesB), 'd')


if __name__ == '__main__':
    unittest.main()
