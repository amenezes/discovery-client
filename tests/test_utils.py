import unittest

from discovery.utils import select_one_randomly, select_one_rr


class TestUtils(unittest.TestCase):

    def test_select_one_randomly(self):
        services = ['a', 'b', 'c']

        self.assertIn(select_one_randomly(services), services)

    def test_select_one_rr(self):
        services = ['a', 'b', 'c']

        self.assertEqual('a', select_one_rr(services))
        self.assertEqual('b', select_one_rr(services))
        self.assertEqual('c', select_one_rr(services))

        self.assertEqual('a', select_one_rr(services))
        self.assertEqual('b', select_one_rr(services))
        self.assertEqual('c', select_one_rr(services))


if __name__ == '__main__':
    unittest.main()
