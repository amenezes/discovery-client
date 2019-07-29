import json
import unittest

from discovery.api.coordinate import Coordinate
from discovery.core.engine.standard import StandardEngine


class TestCoordinate(unittest.TestCase):

    def get_sample_payload(self):
        return json.dumps({
            'Node': 'agent-one',
            'Segment': '',
            'Coord': {
                'Adjustment': 0,
                'Error': 1.5,
                'Height': 0,
                'Vec': [0, 0, 0, 0, 0, 0, 0, 0]
            }
        })

    def get_node(self):
        response = self.coordinate.read_lan()
        return response.json()[0].get('Node')

    def setUp(self):
        client = StandardEngine()
        self.coordinate = Coordinate(client)

    def test_read_wan(self):
        response = self.coordinate.read_wan()
        self.assertTrue(response.ok)

    def test_read_lan(self):
        response = self.coordinate.read_lan()
        self.assertTrue(response.ok)

    def test_read_lan_node(self):
        response = self.coordinate.read_lan_node(self.get_node())
        self.assertTrue(response.ok)

    def test_update_lan_node(self):
        response = self.coordinate.update_lan_node(self.get_sample_payload())
        self.assertTrue(response.ok)
