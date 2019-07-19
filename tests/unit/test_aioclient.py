"""Test Consul async client module."""

import asyncio

import asynctest
from asynctest import CoroutineMock, patch

import consul.aio

from discovery import aioclient, check, service
from discovery.utils import select_one_random


class TestAioClient(asynctest.TestCase):
    """Unit tests to async Consul client."""

    @patch('discovery.aioclient.consul.aio.Consul')
    async def setUp(self, MockAioConsul):
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
                 'ID': '5d9f029a-ee3f-b8b6-61a9-4042ad43e968',
                 'Address': '127.0.0.1',
                 'ServiceID': '#123',
                 'ServiceName': 'consul',
                 'ServicePort': 8300}])
        self.myapp_raw_response = (
            0, [{'Node': 'localhost',
                 'ID': '5d9f029a-ee3f-b8b6-61a9-4042ad43e968',
                 'Address': '127.0.0.1',
                 'ServiceID': '#987',
                 'ServiceName': 'myapp',
                 'ServicePort': 5000}])
        self.fmt_response = [
            {
                'node': 'localhost',
                'node_id': '5d9f029a-ee3f-b8b6-61a9-4042ad43e968',
                'address': '127.0.0.1',
                'service_id': '#123',
                'service_name': 'consul',
                'service_port': 8300
            },
            {
                'node': 'localhost',
                'node_id': '5d9f029a-ee3f-b8b6-61a9-4042ad43e968',
                'address': '127.0.0.1',
                'service_id': '#987',
                'service_name': 'myapp',
                'service_port': 5000
            }]

        self.consul_client = MockAioConsul(consul.aio.Consul)
        self.consul_client.agent.service.register = CoroutineMock()
        self.consul_client.agent.service.deregister = CoroutineMock()
        self.consul_client.status.leader = CoroutineMock(
            return_value='127.0.0.1:8300'
        )
        self.consul_client.health.service = CoroutineMock(
            return_value=self.consul_health_response
        )
        self.consul_client.catalog.service = CoroutineMock(
            return_value=self.consul_raw_response
        )
        self.svc = service.Service(
            'myapp',
            5000,
            check=check.Check('test-check', check.alias('consul'))
        )
        self.dc = aioclient.Consul()
        self.dc.service = self.svc

    async def test_default_timeout(self):
        """Test the default timeout used to check periodically health status of the Consul connection."""
        self.assertEqual(self.dc.timeout, 30)

    async def test_changing_default_timeout(self):
        """Test change the time used to check periodically health status of the Consul connection."""
        self.dc.timeout = '5'
        self.assertNotEqual(self.dc.timeout, 30)

    async def test_find_services(self):
        """Test for localization of a set of services present in the consul's catalog.

        Return a list of instances present in the consul's catalog.
        """
        consul_service = await self.dc.find_service('consul')

        self.assertIsInstance(consul_service, service.Service)
        self.assertEqual(consul_service.raw, self.fmt_response[0])

    async def test_find_services_not_on_catalog(self):
        """Test for localization of a set of services not present in the consul's catalog.

        Return a empty list.
        """
        self.consul_client.catalog.service = CoroutineMock(
            return_value=(0, [])
        )
        response = await self.dc.find_services('myapp')

        self.assertEqual(response, [])

    async def test_test_find_service_random(self):
        """Test for localization of a service present in the consul's catalog.

        Return random instances, when there is more than one registered.
        """
        consul_service = await self.dc.find_service(
            'consul', select_one_random
        )

        self.assertIsInstance(consul_service, service.Service)
        self.assertIn(consul_service.raw, self.fmt_response)

    async def test_leader_current_id(self):
        """Test retrieve the ID from Consul leader."""
        current_id = await self.dc.leader_current_id()

        self.assertIsNotNone(current_id)
        self.assertEqual(
            current_id,
            self.consul_health_response[1][0]['Node']['ID']
        )

    async def test_register(self):
        """Test registration of a service in the  consul's catalog."""
        await self.dc.register()
        myapp_service = await self.dc.find_service('myapp')

        self.assertIsInstance(myapp_service, service.Service)
        self.assertIn(myapp_service.raw, self.fmt_response)

    async def test_deregister(self):
        """Test the deregistration of a service present in the consul's catalog."""
        await self.dc.register()
        await self.dc.deregister()

        self.consul_client.catalog.service = CoroutineMock(
            return_value=(0, [])
        )

        with self.assertRaises(IndexError):
            await self.dc.find_service('myapp')

    async def test_register_additional_check(self):
        """Test the registration of an additional check for a service registered."""
        await self.dc.register_additional_check(
            check.Check(
                name='additional-check',
                check=check.alias('consul')
            )
        )

    async def test_register_additional_check_failed(self):
        with self.assertRaises(TypeError):
            await self.dc.register_additional_check('invalid-check')

    async def test_deregister_additional_check(self):
        """Test the registration of an additional check for a service registered."""
        await self.dc.deregister_additional_check(
            check.Check(
                name='additional-check',
                check=check.alias('consul')
            )
        )

    async def test_deregister_additional_check_failed(self):
        with self.assertRaises(TypeError):
            await self.dc.deregister_additional_check('invalid-check')