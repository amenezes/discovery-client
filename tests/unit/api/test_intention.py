import json
import unittest

from discovery.api.intention import Intentions
from discovery.core.engine.standard import StandardEngine


class TestIntentions(unittest.TestCase):

    def get_sample_payload(self):
        return json.dumps({
            'SourceName': 'web',
            'DestinationName': 'db',
            'SourceType': 'consul',
            'Action': 'allow'
        })

    def get_update_payload(self):
        return json.dumps({
            'SourceName': 'web',
            'DestinationName': 'other-db',
            'SourceType': 'consul',
            'Action': 'allow'
        })

    def clean_state(self):
        response = self.intention.list()
        if len(response.json()) > 0:
            self.intention.delete(response.json()[0].get('ID'))

    def create_sample(self):
        response = self.intention.list()
        if len(response.json()) == 0:
            self.intention.create(self.get_sample_payload())

    def get_intention_uuid(self):
        response = self.intention.list()
        return response.json()[0].get('ID')

    def setUp(self):
        client = StandardEngine()
        self.intention = Intentions(client)
        self.create_sample()

    def tearDown(self):
        self.clean_state()

    def test_create(self):
        self.clean_state()
        response = self.intention.create(self.get_sample_payload())
        self.assertTrue(response.ok)

    def test_read(self):
        response = self.intention.read(self.get_intention_uuid())
        self.assertTrue(response.ok)

    def test_list(self):
        response = self.intention.list()
        self.assertTrue(response.ok)

    def test_update(self):
        response = self.intention.update(
            self.get_intention_uuid(),
            self.get_update_payload()
        )
        self.assertTrue(response.ok)

    def test_delete(self):
        response = self.intention.delete(self.get_intention_uuid())
        self.assertTrue(response.ok)

    def test_check(self):
        response = self.intention.check('web', 'db')
        self.assertTrue(response.ok)

    def test_match_success(self):
        response = self.intention.match('source', 'web')
        self.assertTrue(response.ok)

    def test_match_value_error(self):
        with self.assertRaises(ValueError):
            self.intention.match('web', 'web')
