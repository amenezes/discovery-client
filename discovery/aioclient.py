"""Async consul discovery client module."""

import asyncio
import logging

import aiohttp

import consul.aio

from discovery.base_client import BaseClient
from discovery.filter import Filter
from discovery.utils import select_one_randomly, select_one_rr


logging.getLogger(__name__).addHandler(logging.NullHandler())


class Consul(BaseClient):
    """Async Consul Service Registry."""

    def __init__(self, host, port, app):
        """Create a instance for async consul client."""
        super().__init__()
        self.__discovery = consul.aio.Consul(host, port, loop=app)

    async def _reconnect(self, service):
        """Service re-registration steps."""
        await self.__discovery.agent.service.deregister(service.id)
        await self.__discovery.agent.service.register(
            name=service.name,
            service_id=service.id,
            check=service.healthcheck,
            address=service.ip,
            port=service.port
        )

        self.__id = await self.get_leader_current_id()

        logging.debug(f"Consul ID: {self.__id}")
        logging.info('Service successfully re-registered')

    async def get_leader_current_id(self):
        """Retrieve current ID from consul leader."""
        consul_leader = await self.__discovery.status.leader()
        consul_instances = await self.__discovery.health.service('consul')
        consul_instances = consul_instances[Filter.PAYLOAD.value]

        current_id = [instance['Node']['ID']
                      for instance in consul_instances
                      if instance['Node']['Address'] == consul_leader.split(':')[0]]

        return current_id[Filter.FIRST_ITEM.value]

    async def check_consul_health(self, service):
        """Start a loop that check consul health.

        Necessary to re-register service in case of consul fail.
        """
        while True:
            try:
                await asyncio.sleep(self.DEFAULT_TIMEOUT)
                current_id = await self.get_leader_current_id()
                logging.debug(f"Consul ID: {current_id}")

                if current_id != self.__id:
                    await self._reconnect(service)

            except aiohttp.ClientConnectorError:
                logging.error('failed to connect to discovery service...')
                logging.error(
                    f"reconnect will occur in {self.DEFAULT_TIMEOUT} seconds."
                )
                await self.check_consul_health(service)

            except aiohttp.ServerDisconnectedError:
                logging.error(
                    'temporary loss of communication with the discovery server.'
                )
                asyncio.sleep(self.DEFAULT_TIMEOUT)
                await self.check_consul_health(service)

    async def find_service(self, name, method='rr'):
        """Search for a service in the consul's catalog.

        Return a specific service using: round robin (default) or random.
        """
        services = await self.find_services(name)

        if method == 'rr':
            service = select_one_rr(name, services)
        else:
            service = select_one_randomly(services)

        return service

    async def find_services(self, name):
        """
        Search for a service in the consul's catalog.

        Return a list of services registered on consul catalog.
        """
        services = await self.__discovery.catalog.service(name)
        return self._format_catalog_service(services)

    async def deregister(self, service):
        """Deregister a service registered."""
        await self.__discovery.agent.service.deregister(service.id)
        logging.info('successfully unregistered application!')

    async def register(self, service):
        """Register a new service."""
        try:
            await self.__discovery.agent.service.register(
                name=service.name,
                service_id=service.id,
                check=service.healthcheck,
                address=service.ip,
                port=service.port
            )

            self.__id = await self.get_leader_current_id()

            logging.info('service successfully registered!')
            logging.debug(f"Consul ID: {self.__id}")

        except aiohttp.ClientConnectorError:
            logging.error("Failed to connect to discovery...")

    async def append_healthcheck(self, service, check):
        """Append a healthcheck to a service registered."""
        await self.__discovery.agent.check.register(
            check.name, check.value, service_id=service.id)

    async def remove_healthcheck(self, service, check):
        """Remove a healthcheck to a service registered."""
        await self.__discovery.agent.check.deregister(check.id)
