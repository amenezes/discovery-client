import unittest
from unittest.mock import MagicMock, patch

from discovery.api.segment import Segment
from discovery.core.engine.standard import StandardEngine


class TestSegment(unittest.TestCase):

    @patch('discovery.core.engine.standard.requests.Session')
    def setUp(self, RequestsMock):
        session = RequestsMock()
        session.get = MagicMock(return_value=["", "alpha", "beta"])
        client = StandardEngine(session=session)
        self.segment = Segment(client=client)

    def test_list(self):
        response = self.segment.list()
        self.assertEqual(response, ["", "alpha", "beta"])
