"""Consul discovery client module"""

import consul
import uuid
import socket
import requests

from discovery.filter import Filter

import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(logging.NullHandler())


class Consul:
    """ Consul Service Registry """

    __id = ''
    __service = {'application_ip': socket.gethostbyname(socket.gethostname())}

    def __init__(self, host, port):
        self.__discovery = consul.Consul(host, port)

    def __create_service(self, service_name, service_port, healthcheck_path):
        """Adjusts the data of the service to be managed"""
        self.__service.update({'name': service_name})
        self.__service.update({'port': int(service_port)})
        self.__service.update({'id': f"{service_name}-{uuid.uuid4().hex}"})
        self.__service.update({'healthcheck': {
            "http": f"http://{service_name}:{service_port}{healthcheck_path}",
            "DeregisterCriticalServiceAfter": "1m",
            "interval": "10s",
            "timeout": "5s"}})

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

    def __reconnect(self):
        """service re-registration steps"""
        logging.debug('Service reconnect fallback')

        self.__discovery.agent.service.deregister(self.__service['id'])
        self.__discovery.agent.service.register(name=self.__service['name'],
                                                service_id=self.__service['id'],
                                                check=self.__service['healthcheck'],
                                                address=self.__service['application_ip'],
                                                port=self.__service['port'])
        current_id = self.__discovery.health.service('consul')
        self.__id = self.__format_id(current_id)

        logging.info('Service successfully re-registered')

    def consul_is_healthy(self):
        """Start a loop to monitor consul healthy re-registering
        service in case of consul fail"""
        try:
            current_id = self.__discovery.health.service('consul')
            logging.debug('Checking consul health status')
            logging.debug('Consul ID: %s' % self.__format_id(current_id))

            if self.__format_id(current_id) != self.__id:
                self.__reconnect()

        except requests.exceptions.ConnectionError:
            logging.error(f"Failed to connect to discovery service...")
            logging.info('Reconnect will occur in 5 seconds.')

    def find_service(self, service_name):
        """Search for a service in the consul's catalog"""
        services = self.__discovery.catalog.service(service_name)
        return self.__format_catalog_service(services)

    def deregister(self):
        """Deregister a service registered"""
        logging.debug('Unregistering service id: %s' % self.__service['id'])
        logging.info('Successfully unregistered application!')

        self.__discovery.agent.service.deregister(self.__service['id'])

    def register(self, service_name, service_port, healthcheck_path="/manage/health"):
        """Register a new service with:
        healthcheck path: /mange/health
        DeregisterCriticalServiceAfter: 1m,
        interval: 10s,
        timeout: 5s
        """
        try:
            self.__create_service(service_name,
                                  service_port,
                                  healthcheck_path)
            self.__discovery.agent.service.register(name=self.__service['name'],
                                                    service_id=self.__service['id'],
                                                    check=self.__service['healthcheck'],
                                                    address=self.__service['application_ip'],
                                                    port=self.__service['port'])
            current_id = self.__discovery.health.service('consul')
            self.__id = self.__format_id(current_id)

            logging.info('Service successfully registered!')
            logging.debug('Consul ID: %s' % self.__id)

        except requests.exceptions.ConnectionError:
            logging.error(f"Failed to connect to discovery...")
