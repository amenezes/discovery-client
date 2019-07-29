"""Async consul discovery client module."""

import asyncio
import logging

import aiohttp

import attr

from discovery.base_client import BaseClient
from discovery.check import Check
from discovery.core.engine.aio import AioEngine
from discovery.core.engine.base import Engine
from discovery.exceptions import ServiceNotFoundException
from discovery.filter import Filter
from discovery.utils import select_one_rr


logging.getLogger(__name__).addHandler(logging.NullHandler())


@attr.s(slots=True)
class Consul(BaseClient):
    """Async Consul Service Registry."""

    app = attr.ib(default=asyncio.get_event_loop())
    client = attr.ib(
        type=Engine,
        default=AioEngine(),
        validator=attr.validators.instance_of(Engine)
    )

    async def reconnect(self):
        """Service re-registration steps."""
        await self.agent.service.deregister(self.service.identifier)
        await self.agent.service.register(
            name=self.service.name,
            service_id=self.service.identifier,
            check=self.service.check,
            address=self.service.ip,
            port=self.service.port
        )

        self.__id = await self.leader_current_id()

        logging.debug(f"Consul ID: {self.__id}")
        logging.info('Service successfully re-registered')

    async def get_leader_ip(self):
        leader_response = await self.status.leader()
        leader_response = await leader_response.json()
        consul_leader, _ = leader_response.split(':')
        return consul_leader

    async def get_consul_health(self):
        health_response = await self.health.service('consul')
        consul_instances = await health_response.json()
        return consul_instances

    async def leader_current_id(self):
        """Retrieve current ID from consul leader."""
        consul_leader = await self.get_leader_ip()
        consul_instances = await self.get_consul_health()

        current_id = [instance.get('Node').get('ID')
                      for instance in consul_instances
                      if instance.get('Node').get('Address') == consul_leader]

        if current_id is not None:
            current_id = current_id[Filter.FIRST_ITEM.value]

        return current_id

    async def check_consul_health(self):
        """Start a loop that check consul health.

        Necessary to re-register service in case of consul fail.
        """
        while True:
            try:
                await asyncio.sleep(self.timeout)
                current_id = await self.leader_current_id()
                logging.debug(f"Consul ID: {current_id}")

                if current_id != self.__id:
                    await self.reconnect(self.service)

            except aiohttp.ClientConnectorError:
                logging.error('failed to connect to discovery service...')
                logging.error(
                    f"reconnect will occur in {self.timeout} seconds."
                )
                await self.check_consul_health(self.service)

            except aiohttp.ServerDisconnectedError:
                logging.error(
                    'temporary loss of communication with the discovery server.'
                )
                asyncio.sleep(self.timeout)
                await self.check_consul_health(self.service)

    async def find_service(self, name, fn=select_one_rr):
        """Search for a service in the consul's catalog."""
        response = await self.find_services(name)
        if not response.status == 200:
            raise ServiceNotFoundException
        services = await response.json()
        return fn(services)

    async def find_services(self, name):
        """Search for a service in the consul's catalog."""
        services = await self.catalog.service(name)
        return services

    async def deregister(self):
        """Deregister a service registered."""
        await self.__discovery.agent.service.deregister(self.service.identifier)
        logging.info('successfully unregistered application!')

    async def register(self):
        """Register a new service."""
        try:
            await self.__discovery.agent.service.register(
                name=self.service.name,
                service_id=self.service.identifier,
                check=self.service.check.value,
                address=self.service.ip,
                port=self.service.port
            )

            self.__id = await self.leader_current_id()

            logging.info('service successfully registered!')
            logging.debug(f"Consul ID: {self.__id}")

        except aiohttp.ClientConnectorError:
            logging.error("Failed to connect to discovery...")

    async def register_additional_check(self, check):
        """Append a Consul's check to a service registered."""
        if not isinstance(check, Check):
            raise TypeError('check must be Check instance.')

        self.__discovery.agent.check.register(
            check.name, check.value, service_id=self.service.identifier
        )

    async def deregister_additional_check(self, check):
        """Remove a Consul's check to a service registered."""
        if not isinstance(check, Check):
            raise TypeError('check must be Check instance.')

        self.__discovery.agent.check.deregister(check.identifier)
