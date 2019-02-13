"""Async consul discovery client module"""

import consul.aio
import logging
import uuid
import socket
import asyncio
import aiohttp

from discovery.filter import Filter

import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(logging.NullHandler())


class Consul:
    """ Async Consul Service Registry """

    __id = ''
    __service = {}

    def __init__(self, host, port, app):
        self.__discovery = consul.aio.Consul(host, port, loop=app)

    def __create_service(self, service_name, service_port, healthcheck_path):
        """Adjusts the data of the service to be managed"""
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
        """Retrieve consul ID from
        Consul API: /health/status/<service>
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
        """Start a loop to monitor consul healthy
        re-registering service in case of consul fail"""
        while True:
            try:
                await asyncio.sleep(5)
                current_id = await self.__discovery.health.service('consul')

                if self.__format_id(current_id) != self.__id:
                    await self._reconnect()

            except aiohttp.ClientConnectorError:
                logging.error(f"failed to connect to discovery service...")
                logging.info('reconnect will occur in 5 seconds.')

    async def find_service(self, service_name):
        """List nodes for a service"""
        services = await self.__discovery.catalog.service(service_name)
        return self.__format_catalog_service(services)

    async def deregister(self):
        """Deregister a service registered"""
        await self.__discovery.agent.service.deregister(self.__service['id'])

        logging.info('successfully unregistered application!')

    async def register(self, service_name, service_port, healthcheck_path="/manage/health"):
        """Register a new service, with health check.
        Default health check path: /mange/health
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
