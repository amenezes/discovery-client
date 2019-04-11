"""Async consul discovery client module."""

import asyncio
import logging
import os
import socket
import uuid

import aiohttp

import consul.aio

from discovery.filter import Filter
from discovery.utils import select_one_randomly, select_one_rr


logging.getLogger(__name__).addHandler(logging.NullHandler())


class Consul:
    """Async Consul Service Registry."""

    __id = ''
    __service = {}
    DEFAULT_TIMEOUT = int(Filter.DEFAULT_TIMEOUT.value)

    def __init__(self, host, port, app):
        """Create a instance for async consul client."""
        self.__discovery = consul.aio.Consul(host, port, loop=app)
        if os.getenv('DEFAULT_TIMEOUT'):
            self.DEFAULT_TIMEOUT = int(os.getenv('DEFAULT_TIMEOUT'))

    def __create_service(self, service_name, service_port, healthcheck_path):
        """Adjust the data of the service to be managed."""
        self.__service.update({'name': service_name})
        self.__service.update({'port': int(service_port)})
        self.__service.update({'id': f"{service_name}-{uuid.uuid4().hex}"})
        self.__service.update(
            {'application_ip': socket.gethostbyname(socket.gethostname())})
        self.__service.update({'healthcheck': {
            "http": f"http://{service_name}:{service_port}{healthcheck_path}",
            "DeregisterCriticalServiceAfter": "1m",
            "interval": "10s",
            "timeout": "5s"
        }})

        logging.debug(f'Service data: {self.__service}')

    def __format_catalog_service(self, services):
        servicesfmt = [{"node": svc['Node'],
                        "address": svc['Address'],
                        "service_id": svc['ServiceID'],
                        "service_name": svc['ServiceName'],
                        "service_port": svc['ServicePort']}
                       for svc in services[Filter.PAYLOAD.value]]
        return servicesfmt

    async def _reconnect(self):
        """Service re-registration steps."""
        await self.__discovery.agent.service.deregister(self.__service['id'])
        await self.__discovery.agent.service.register(
            name=self.__service['name'],
            service_id=self.__service['id'],
            check=self.__service['healthcheck'],
            address=self.__service['application_ip'],
            port=self.__service['port']
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

        # if len(current_id) > 0:
        #     current_id = current_id[Filter.FIRST_ITEM.value]

        return current_id[Filter.FIRST_ITEM.value]

    async def consul_is_healthy(self):
        """Start a loop to monitor consul healthy.

        Necessary to re-register service in case of consul fail.
        """
        while True:
            try:
                await asyncio.sleep(self.DEFAULT_TIMEOUT)
                current_id = await self.get_leader_current_id()

                logging.debug('Checking consul health status')
                logging.debug(f"Consul ID: {current_id}")

                if current_id != self.__id:
                    await self._reconnect()

            except aiohttp.ClientConnectorError:
                logging.error('failed to connect to discovery service...')
                logging.error(
                    f"reconnect will occur in {self.DEFAULT_TIMEOUT} seconds."
                )
                await self.consul_is_healthy()

            except aiohttp.ServerDisconnectedError:
                logging.error(
                    'temporary loss of communication with the discovery server.'
                )
                asyncio.sleep(self.DEFAULT_TIMEOUT)
                await self.consul_is_healthy()

    async def find_service(self, service_name, method='rr'):
        """Search for a service in the consul's catalog.

        Return a specific service using: round robin (default) or random.
        """
        services = await self.find_services(service_name)

        if method == 'rr':
            service = select_one_rr(service_name, services)
        else:
            service = select_one_randomly(services)

        return service

    async def find_services(self, service_name):
        """
        Search for a service in the consul's catalog.

        Return a list of services registered on consul catalog.
        """
        services = await self.__discovery.catalog.service(service_name)
        return self.__format_catalog_service(services)

    async def deregister(self):
        """Deregister a service registered."""
        await self.__discovery.agent.service.deregister(self.__service['id'])

        logging.info('successfully unregistered application!')

    async def register(self,
                       service_name,
                       service_port,
                       healthcheck_path="/manage/health"):
        """Register a new service.

        Default values are:
        healthcheck path: /mange/health
        DeregisterCriticalServiceAfter: 1m,
        interval: 10s,
        timeout: 5s
        """
        try:
            self.__create_service(
                service_name,
                service_port,
                healthcheck_path
            )
            await self.__discovery.agent.service.register(
                name=self.__service['name'],
                service_id=self.__service['id'],
                check=self.__service['healthcheck'],
                address=self.__service['application_ip'],
                port=self.__service['port']
            )

            self.__id = await self.get_leader_current_id()

            logging.info('service successfully registered!')
            logging.debug(f"Consul ID: {self.__id}")

        except aiohttp.ClientConnectorError:
            logging.error("failed to connect to discovery...")
