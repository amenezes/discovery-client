import unittest
from unittest.mock import MagicMock, patch

from discovery.api.agent import Agent
from discovery.core.engine.standard import StandardEngine
from discovery.service import Service


class TestAgent(unittest.TestCase):

    def get_stream_logs_sample(self):
        return [
            'YYYY/MM/DD HH:MM:SS [INFO] raft: Initial configuration (index=1): [{Suffrage:Voter ID:127.0.0.1:8300 Address:127.0.0.1:8300}]',
            'YYYY/MM/DD HH:MM:SS [INFO] raft: Node at 127.0.0.1:8300 [Follower] entering Follower state (Leader: "")',
            'YYYY/MM/DD HH:MM:SS [INFO] serf: EventMemberJoin: machine-osx 127.0.0.1',
            'YYYY/MM/DD HH:MM:SS [INFO] consul: Adding LAN server machine-osx (Addr: tcp/127.0.0.1:8300) (DC: dc1)',
            'YYYY/MM/DD HH:MM:SS [INFO] serf: EventMemberJoin: machine-osx.dc1 127.0.0.1',
            'YYYY/MM/DD HH:MM:SS [INFO] consul: Handled member-join event for server "machine-osx.dc1" in area "wan"'
        ]

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
    @patch('discovery.core.engine.standard.requests.Session')
    def test_stream_logs(self, MockRequests):
        session = MockRequests()
        session.get = MagicMock(return_value=self.get_stream_logs_sample())
        client = StandardEngine(session=session)
        agent = Agent(client)

        response = agent.stream_logs(stream=True)
        self.assertIsNotNone(response)

    def test_join(self):
        response = self.agent.join(self.service.address)
        self.assertIsNotNone(response)

    @patch('discovery.core.engine.standard.requests.Session')
    def test_leave(self, MockRequests):
        session = MockRequests()
        session.put = MagicMock()
        client = StandardEngine(session=session)
        agent = Agent(client)

        response = agent.leave()
        self.assertIsNotNone(response)

    def test_force_leave(self):
        response = self.agent.force_leave(self.service.node)
        self.assertIsNotNone(response)
