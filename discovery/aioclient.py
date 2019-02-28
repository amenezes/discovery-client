"""Async consul discovery client module."""

import asyncio
import logging
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

    def __init__(self, host, port, app):
        """Create a instance for async consul client."""
        self.__discovery = consul.aio.Consul(host, port, loop=app)

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

        logging.debug('Service data: %s' % self.__service)

    def __format_id(self, id):
        """Retrieve consul ID from Consul API: /health/status/<service>.

        docs: https://www.consul.io/api/health.html#list-nodes-for-service
        """
        return id[Filter.PAYLOAD.value][Filter.FIRST_ITEM.value]['Node']['ID']

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
        await self.__discovery.agent.service.register(name=self.__service['name'],
                                                      service_id=self.__service['id'],
                                                      check=self.__service['healthcheck'],
                                                      address=self.__service['application_ip'],
                                                      port=self.__service['port'])
        current_id = await self.__discovery.health.service('consul')
        self.__id = self.__format_id(current_id)

        logging.debug('Consul ID: %s' % self.__format_id(current_id))
        logging.info('Service successfully re-registered')

    async def _consul_is_healthy(self):
        """Start a loop to monitor consul healthy.

        Necessary to re-register service in case of consul fail.
        """
        while True:
            try:
                await asyncio.sleep(5)
                current_id = await self.__discovery.health.service('consul')

                if self.__format_id(current_id) != self.__id:
                    await self._reconnect()

            except aiohttp.ClientConnectorError:
                logging.error(f"failed to connect to discovery service...")
                logging.info('reconnect will occur in 5 seconds.')

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

    async def register(self, service_name, service_port, healthcheck_path="/manage/health"):
        """Register a new service.

        Default values are:
        healthcheck path: /mange/health
        DeregisterCriticalServiceAfter: 1m,
        interval: 10s,
        timeout: 5s
        """
        try:
            self.__create_service(service_name,
                                  service_port,
                                  healthcheck_path)
            await self.__discovery.agent.service.register(name=self.__service['name'],
                                                          service_id=self.__service['id'],
                                                          check=self.__service['healthcheck'],
                                                          address=self.__service['application_ip'],
                                                          port=self.__service['port'])
            current_id = await self.__discovery.health.service('consul')
            self.__id = self.__format_id(current_id)

            logging.info('service successfully registered!')
            logging.debug('Consul ID: %s' % self.__format_id(current_id))

            await self._consul_is_healthy()
        except aiohttp.ClientConnectorError:
            logging.error(f"failed to connect to discovery...")
            await self._consul_is_healthy()