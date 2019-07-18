"""Async consul discovery client module."""

import asyncio
import logging

import aiohttp

import attr

import consul.aio

from discovery.base_client import BaseClient
from discovery.check import Check
from discovery.filter import Filter
from discovery.utils import select_one_rr


logging.getLogger(__name__).addHandler(logging.NullHandler())


@attr.s(kw_only=True)
class Consul(BaseClient):
    """Async Consul Service Registry."""

    _host = attr.ib(type=str, default='localhost')
    _port = attr.ib(type=int, default=8500)
    _app = attr.ib(default=asyncio.get_event_loop())

    def __attrs_post_init__(self):
        self.__discovery = consul.aio.Consul(
            loop=self._app, host=self._host, port=self._port
        )

    def connect(self):
        self.__discovery = consul.Consul(self._host, self._port)
    # def __init__(self, host, port, app):
    #     """Create a instance for async consul client."""
    #     super().__init__()
    #     self.__discovery = consul.aio.Consul(loop=app, host='localhost', port=8500)

    async def _reconnect(self, service):
        """Service re-registration steps."""
        await self.__discovery.agent.service.deregister(service.identifier)
        await self.__discovery.agent.service.register(
            name=service.name,
            service_id=service.identifier,
            check=service.check,
            address=service.ip,
            port=service.port
        )

        self.__id = await self.leader_current_id()

        logging.debug(f"Consul ID: {self.__id}")
        logging.info('Service successfully re-registered')

    async def leader_current_id(self):
        """Retrieve current ID from consul leader."""
        consul_leader = await self.__discovery.status.leader()
        consul_instances = await self.__discovery.health.service('consul')
        consul_instances = consul_instances[Filter.PAYLOAD.value]

        current_id = [instance['Node']['ID']
                      for instance in consul_instances
                      if instance['Node']['Address'] == consul_leader.split(':')[Filter.FIRST_ITEM.value]]

        return current_id[Filter.FIRST_ITEM.value]

    async def check_consul_health(self, service):
        """Start a loop that check consul health.

        Necessary to re-register service in case of consul fail.
        """
        while True:
            try:
                await asyncio.sleep(self.DEFAULT_TIMEOUT)
                current_id = await self.leader_current_id()
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

    async def find_service(self, name, fn=select_one_rr):
        """Search for a service in the consul's catalog."""
        services = await self.find_services(name)
        return fn(services)

    async def find_services(self, name):
        """Search for a service in the consul's catalog."""
        services = await self.__discovery.catalog.service(name)
        return self._format_catalog_service(services)

    async def deregister(self, service):
        """Deregister a service registered."""
        await self.__discovery.agent.service.deregister(service.identifier)
        logging.info('successfully unregistered application!')

    async def register(self, service):
        """Register a new service."""
        try:
            await self.__discovery.agent.service.register(
                name=service.name,
                service_id=service.identifier,
                check=service.check,
                address=service.ip,
                port=service.port)

            self.__id = await self.leader_current_id()

            logging.info('service successfully registered!')
            logging.debug(f"Consul ID: {self.__id}")

        except aiohttp.ClientConnectorError:
            logging.error("Failed to connect to discovery...")

    async def register_additional_check(self, check, service_id):
        """Append a Consul's check to a service registered."""
        if isinstance(check, Check):
            self.__discovery.agent.check.register(
                check.name, check.value, service_id=service_id)
        else:
            raise TypeError('check must be Check instance.')

    async def register_additional_checks(self, service):
        """Append a Consul's check to a service registered."""
        for check in service.additional_checks():
            await self.register_additional_check(check, service.identifier)

    async def deregister_additional_check(self, check_id):
        """Remove a Consul's check to a service registered."""
        self.__discovery.agent.check.deregister(check_id)

    async def deregister_additional_checks(self, service):
        """Remove a Consul's check to a service registered."""
        for check in service.additional_checks():
            await self.deregister_additional_check(check.identifier)
