"""Test Consul async client module."""
import asyncio
import os
import unittest

import asynctest
from asynctest import CoroutineMock, patch

import consul.aio

from discovery.consul import aioclient
from discovery.service import Service


class TestAioClient(asynctest.TestCase):
    """Unit tests to async Consul client."""

    def setUp(self):
        """Mock of responses generated by python-consul.

        and expected results generated by discovery-client.
        """
        self.loop = asyncio.get_event_loop()
        self.consul_health_response = (
            0, [{'Node': {
                'ID': '123456',
                'Address': '127.0.0.1'}}])
        self.consul_raw_response = (
            0, [{'Node': 'localhost',
                 'Address': '127.0.0.1',
                 'ServiceID': '#123',
                 'ServiceName': 'consul',
                 'ServicePort': 8300}])
        self.myapp_raw_response = (
            0, [{'Node': 'localhost',
                 'ID': '987654',
                 'Address': '127.0.0.1',
                 'ServiceID': '#987',
                 'ServiceName': 'myapp',
                 'ServicePort': 5000}])
        self.fmt_response = [
            {
                'node': 'localhost',
                'address': '127.0.0.1',
                'service_id': '#123',
                'service_name': 'consul',
                'service_port': 8300
            },
            {
                'node': 'localhost',
                'address': '127.0.0.1',
                'service_id': '#987',
                'service_name': 'myapp',
                'service_port': 5000
            }]

    def test_default_timeout(self):
        async def async_test_default_timeout(loop):
            del os.environ['DEFAULT_TIMEOUT']
            dc = aioclient.Consul('localhost', 8500, app=loop)

            self.assertEqual(dc.DEFAULT_TIMEOUT, 30)

        self.loop.run_until_complete(
            async_test_default_timeout(self.loop)
        )

    def test_changing_default_timeout(self):
        """Test change the time used to check periodically health status of the Consul connection."""
        async def async_test_changing_default_timeout(loop):
            os.environ['DEFAULT_TIMEOUT'] = '5'
            dc = aioclient.Consul('localhost', 8500, app=loop)

            self.assertEqual(dc.DEFAULT_TIMEOUT, 5)
            self.assertNotEqual(dc.DEFAULT_TIMEOUT, 30)

        self.loop.run_until_complete(
            async_test_changing_default_timeout(self.loop)
        )

    @patch('discovery.consul.aioclient.consul.aio.Consul')
    def test_find_services(self, MockAioConsul):
        """Test for localization of a set of services present in the consul's catalog.

        Return a list of instances present in the consul's catalog.
        """
        async def async_test_find_services(loop):
            consul_client = MockAioConsul(consul.aio.Consul)
            consul_client.catalog.service = CoroutineMock(
                return_value=self.consul_raw_response
            )

            dc = aioclient.Consul('localhost', 8500, app=loop)
            consul_service = await dc.find_service('consul')

            self.assertIsInstance(consul_service, dict)
            self.assertEqual(consul_service, self.fmt_response[0])

        self.loop.run_until_complete(
            async_test_find_services(self.loop)
        )

    @patch('discovery.consul.aioclient.consul.aio.Consul')
    def test_find_services_not_on_catalog(self, MockAioConsul):
        """Test for localization of a set of services not present in the consul's catalog.

        Return a empty list.
        """
        async def async_test_find_services_not_on_catalog(loop):
            consul_client = MockAioConsul(consul.aio.Consul)
            consul_client.catalog.service = CoroutineMock(
                return_value=(0, [])
            )

            dc = aioclient.Consul('localhost', 8500, app=loop)
            response = await dc.find_services('myapp')

            self.assertEqual(response, [])

        self.loop.run_until_complete(
            async_test_find_services_not_on_catalog(self.loop)
        )

    @patch('discovery.consul.aioclient.consul.aio.Consul')
    def test_test_find_service_random(self, MockAioConsul):
        """Test for localization of a service present in the consul's catalog.

        Return random instances, when there is more than one registered.
        """
        async def async_test_find_services(loop):
            consul_client = MockAioConsul(consul.aio.Consul)
            consul_client.catalog.service = CoroutineMock(
                return_value=self.consul_raw_response
            )

            dc = aioclient.Consul('localhost', 8500, app=loop)
            consul_service = await dc.find_service('consul', method='random')

            self.assertIsInstance(consul_service, dict)
            self.assertEqual(consul_service, self.fmt_response[0])

        self.loop.run_until_complete(
            async_test_find_services(self.loop)
        )

    @patch('discovery.consul.aioclient.consul.aio.Consul')
    def test_get_leader_current_id(self, MockAioClient):
        """Test retrieve the ID from Consul leader."""
        async def async_test_get_leader_current_id(loop):
            consul_client = MockAioClient(consul.aio.Consul)
            consul_client.status.leader = CoroutineMock(
                return_value='127.0.0.1:8300'
            )
            consul_client.health.service = CoroutineMock(
                return_value=self.consul_health_response
            )

            dc = aioclient.Consul('localhost', 8500, app=loop)
            current_id = await dc.get_leader_current_id()

            self.assertIsNotNone(current_id)
            self.assertEqual(
                current_id,
                self.consul_health_response[1][0]['Node']['ID']
            )

        self.loop.run_until_complete(
            async_test_get_leader_current_id(self.loop)
        )

    @patch('discovery.consul.aioclient.consul.aio.Consul')
    def test_register(self, MockAioConsul):
        """Test registration of a service in the  consul's catalog."""
        async def async_test_register(loop):
            consul_client = MockAioConsul(consul.aio.Consul)
            consul_client.agent.service.register = CoroutineMock()
            consul_client.status.leader = CoroutineMock(
                return_value='127.0.0.1:8300'
            )
            consul_client.health.service = CoroutineMock(
                return_value=self.consul_health_response
            )
            consul_client.catalog.service = CoroutineMock(
                return_value=self.myapp_raw_response
            )

            svc = Service('myapp', 5000)
            dc = aioclient.Consul('localhost', 8500, app=loop)
            await dc.register(svc)
            myapp_service = await dc.find_service('myapp')

            self.assertIsInstance(myapp_service, dict)
            self.assertEqual(myapp_service, self.fmt_response[1])

        self.loop.run_until_complete(
            async_test_register(self.loop)
        )

    @patch('discovery.consul.aioclient.consul.aio.Consul')
    def test_deregister(self, MockAioConsul):
        """Test the deregistration of a service present in the consul's catalog."""
        async def async_test_deregister(loop):
            consul_client = MockAioConsul(consul.aio.Consul)
            consul_client.agent.service.register = CoroutineMock()
            consul_client.agent.service.deregister = CoroutineMock()
            consul_client.catalog.service = CoroutineMock(
                return_value=self.myapp_raw_response
            )
            consul_client.status.leader = CoroutineMock(
                return_value='127.0.0.1:8300'
            )
            consul_client.health.service = CoroutineMock(
                return_value=self.consul_health_response
            )

            svc = Service('myapp', 5000)
            dc = aioclient.Consul('localhost', 8500, app=loop)
            await dc.register(svc)
            myapp_service = await dc.find_service('myapp')

            self.assertIsInstance(myapp_service, dict)
            self.assertEqual(myapp_service, self.fmt_response[1])

            await dc.deregister(svc)

            consul_client.catalog.service = CoroutineMock(
                return_value=(0, [])
            )

            with self.assertRaises(IndexError):
                await dc.find_service('myapp')

        self.loop.run_until_complete(
            async_test_deregister(self.loop)
        )


if __name__ == '__main__':
    unittest.main()
