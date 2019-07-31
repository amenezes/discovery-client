import unittest
from unittest.mock import MagicMock, patch

from discovery.api.binding_rule import BindingRule
from discovery.core.engine.standard import StandardEngine


class TestBindingRule(unittest.TestCase):

    def get_sample_payload(self):
        return {
            'Description': 'example rule',
            'AuthMethod': 'minikube',
            'Selector': 'serviceaccount.namespace==default',
            'BindType': 'service',
            'BindName': '{{ serviceaccount.name }}'
        }

    def get_rule_id(self):
        response = self.get_sample_response()
        return response.get('ID')

    def get_sample_response(self):
        return {
            'ID': '000ed53c-e2d3-e7e6-31a5-c19bc3518a3d',
            'Description': 'example rule',
            'AuthMethod': 'minikube',
            'Selector': 'serviceaccount.namespace==default',
            'BindType': 'service',
            'BindName': '{{ serviceaccount.name }}',
            'CreateIndex': 17,
            'ModifyIndex': 17
        }

    @patch('discovery.core.engine.standard.requests.Session')
    def setUp(self, RequestsMock):
        self.session = RequestsMock()
        self.session.get = MagicMock(return_value=self.get_sample_response())
        self.session.put = MagicMock(return_value=self.get_sample_response())
        self.session.delete = MagicMock(return_value=True)
        client = StandardEngine(session=self.session)
        self.binding_rule = BindingRule(client)

    def test_create(self):
        response = self.binding_rule.create(self.get_sample_payload())
        self.assertIsInstance(response, dict)

    def test_read(self):
        response = self.binding_rule.read(self.get_rule_id())
        self.assertIsInstance(response, dict)

    def test_update(self):
        response = self.binding_rule.update(
            self.get_rule_id(),
            self.get_sample_payload()
        )
        self.assertIsInstance(response, dict)

    def test_delete(self):
        response = self.binding_rule.delete(self.get_rule_id())
        self.assertTrue(response)

    def test_list(self):
        response = self.binding_rule.list()
        self.assertIsInstance(response, dict)
