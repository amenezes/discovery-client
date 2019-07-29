import asyncio
import unittest

from discovery.core.engine.aio import AioEngine


class TestAioEngine(unittest.TestCase):

    def execute_request(self, method):
        response = self.loop.run_until_complete(
            method
        )
        return response.status

    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.client = AioEngine()

    def test_url(self):
        self.assertEqual(self.client.url, 'http://localhost:8500')

    def test_get(self):
        response = self.execute_request(
            self.client.get('https://httpbin.org/get')
        )
        self.assertEqual(response, 200)

    def test_put(self):
        response = self.execute_request(
            self.client.put('https://httpbin.org/put')
        )
        self.assertEqual(response, 200)

    def test_delete(self):
        response = self.execute_request(
            self.client.delete('https://httpbin.org/delete')
        )
        self.assertEqual(response, 200)

    def test_post(self):
        response = self.execute_request(
            self.client.post('https://httpbin.org/post')
        )
        self.assertEqual(response, 200)
