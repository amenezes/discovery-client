"""Test utils module."""
import unittest

from discovery.utils import select_one_randomly, select_one_rr


class TestUtils(unittest.TestCase):
    """Unit tests to utils module."""

    def test_select_one_randomly(self):
        """Tests the random selection of an instance in a list."""
        services = ['a', 'b', 'c']

        self.assertIn(select_one_randomly(services), services)
        self.assertIn(select_one_randomly(services), services)
        self.assertIn(select_one_randomly(services), services)

    def test_select_one_rr(self):
        """Tests the round robin return of instances present in a list."""
        # group 1: select single service
        serviceA = 'serviceA'
        servicesA = ['a', 'b', 'c']

        self.assertEqual('a', select_one_rr(serviceA, servicesA))
        self.assertEqual('b', select_one_rr(serviceA, servicesA))
        self.assertEqual('c', select_one_rr(serviceA, servicesA))
        self.assertEqual('a', select_one_rr(serviceA, servicesA))

        # group 2: select alternate services
        serviceB = 'serviceB'
        servicesB = ['d', 'e']

        serviceC = 'serviceC'
        servicesC = ['f', 'g', 'h']

        self.assertEqual('d', select_one_rr(serviceB, servicesB))
        self.assertEqual('f', select_one_rr(serviceC, servicesC))
        self.assertEqual('g', select_one_rr(serviceC, servicesC))
        self.assertEqual('e', select_one_rr(serviceB, servicesB))
        self.assertEqual('d', select_one_rr(serviceB, servicesB))

    def test_select_one_rr_exception(self):
        """Test raise IndexError for empty instances present on consul's catalog."""
        service = 'service_name'
        instances = ['a', 'b']

        self.assertEqual('a', select_one_rr(service, instances))
        with self.assertRaises(IndexError):
            select_one_rr(service, [])


if __name__ == '__main__':
    unittest.main()
