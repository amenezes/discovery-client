import unittest

from discovery.api.events import Events
from discovery.core.engine.standard import StandardEngine


class TestEvent(unittest.TestCase):

    def get_sample_payload(self):
        return 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'

    def setUp(self):
        client = StandardEngine()
        self.events = Events(client)

    def test_fire(self):
        response = self.events.fire('my-event', self.get_sample_payload())
        self.assertIsNotNone(response)
        self.assertIsInstance(response.json(), dict)

    def test_list(self):
        response = self.events.list('my-event')
        self.assertIsNotNone(response)
        self.assertIsInstance(response.json(), list)
