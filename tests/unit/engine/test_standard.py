import unittest

from discovery.core.engine.standard import StandardEngine


class TestStandardEngine(unittest.TestCase):

    def setUp(self):
        self.client = StandardEngine()

    def test_url(self):
        self.assertEqual(self.client.url, 'http://localhost:8500')

    def test_get(self):
        response = self.client.get('https://httpbin.org/get')
        self.assertTrue(response.ok)

    def test_put(self):
        response = self.client.put('https://httpbin.org/put')
        self.assertTrue(response.ok)

    def test_delete(self):
        response = self.client.delete('https://httpbin.org/delete')
        self.assertTrue(response.ok)

    def test_post(self):
        response = self.client.post('https://httpbin.org/post')
        self.assertTrue(response.ok)
