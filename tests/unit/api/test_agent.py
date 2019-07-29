import unittest

from discovery.api.agent import Agent
from discovery.core.engine.standard import StandardEngine
from discovery.service import Service


class TestAgent(unittest.TestCase):

    def setUp(self):
        client = StandardEngine()
        self.agent = Agent(client)
        self.service = Service('myapp', 5000)

    def test_members(self):
        response = self.agent.members()
        self.assertIsNotNone(response)
        self.assertTrue(response.ok)

    def test_self(self):
        response = self.agent.self()
        self.assertIsNotNone(response)
        self.assertTrue(response.ok)

    def test_reload(self):
        response = self.agent.reload()
        self.assertTrue(response.ok)

    def test_maintenance(self):
        response = self.agent.maintenance()
        self.assertTrue(response.ok)

    def test_metrics(self):
        response = self.agent.metrics()
        self.assertIsNotNone(response)
        self.assertTrue(response.ok)

    @unittest.skip
    def test_monitor(self):
        self.agent.monitor()

    def test_join(self):
        response = self.agent.join(self.service.address)
        self.assertIsNotNone(response)

    @unittest.skip
    def test_leave(self):
        self.agent.leave()

    def test_force_leave(self):
        response = self.agent.force_leave(self.service.node)
        self.assertIsNotNone(response)
