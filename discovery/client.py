"""Consul discovery client module."""
import logging
import socket
import time
import uuid

import consul

from discovery.base_client import BaseClient
from discovery.filter import Filter
from discovery.utils import select_one_randomly, select_one_rr

import requests


logging.getLogger(__name__).addHandler(logging.NullHandler())


class Consul(BaseClient):
    """Consul Service Registry."""

    __service = {'application_ip': socket.gethostbyname(socket.gethostname())}

    def __init__(self, host, port):
        """Create a instance for standard consul client."""
        super().__init__()
        self.__discovery = consul.Consul(host, port)
        self.__ensure_leader_connection(port)

    def __ensure_leader_connection(self, port):
        leader = self.__discovery.status.leader()
        leader = leader.split(':')
        self.__discovery = consul.Consul(f"{leader[0]}", port)

    def __create_service(self, service_name, service_port, healthcheck_path):
        """Adjust the data of the service to be managed."""
        self.__service.update({'name': service_name})
        self.__service.update({'port': int(service_port)})
        self.__service.update({'id': f"{service_name}-{uuid.uuid4().hex}"})
        self.__service.update({'healthcheck': {
            "http": f"http://{service_name}:{service_port}{healthcheck_path}",
            "DeregisterCriticalServiceAfter": "1m",
            "interval": "10s",
            "timeout": "5s"}})

        logging.debug(f'Service data: {self.__service}')

    def __reconnect(self):
        """Service re-registration steps."""
        logging.debug('Service reconnect fallback')

        self.__discovery.agent.service.deregister(self.__service['id'])
        self.__discovery.agent.service.register(
            name=self.__service['name'],
            service_id=self.__service['id'],
            check=self.__service['healthcheck'],
            address=self.__service['application_ip'],
            port=self.__service['port']
        )

        self.__id = self.get_leader_current_id()

        logging.info('Service successfully re-registered')

    def get_leader_current_id(self):
        """Retrieve current ID from consul leader."""
        consul_leader = self.__discovery.status.leader()
        consul_instances = self.__discovery.health.service('consul')[Filter.PAYLOAD.value]
        current_id = [instance['Node']['ID']
                      for instance in consul_instances
                      if instance['Node']['Address'] == consul_leader.split(':')[0]]

        if len(current_id) > 0:
            current_id = current_id[Filter.FIRST_ITEM.value]

        return current_id

    def consul_is_healthy(self):
        """Start a loop to monitor consul healthy.

        Necessary to re-register service in case of consul fail.
        """
        while True:
            try:
                time.sleep(self.DEFAULT_TIMEOUT)

                current_id = self.get_leader_current_id()
                logging.debug(f"Consul ID: {current_id}")

                if current_id != self.__id:
                    self.__reconnect()

            except requests.exceptions.ConnectionError:
                logging.error("Failed to connect to discovery service...")
                logging.error(
                    f'Reconnect will occur in {self.DEFAULT_TIMEOUT} seconds.'
                )

    def find_service(self, service_name, method='rr'):
        """Search for a service in the consul's catalog.

        Return a specific service using: round robin (default) or random.
        """
        services = self.find_services(service_name)

        if method == 'rr':
            service = select_one_rr(service_name, services)
        else:
            service = select_one_randomly(services)
        return service

    def find_services(self, service_name):
        """
        Search for a service in the consul's catalog.

        Return a list of services registered on consul catalog.
        """
        services = self.__discovery.catalog.service(service_name)
        return self._format_catalog_service(services)

    def deregister(self):
        """Deregister a service registered."""
        logging.debug(
            f"Unregistering service id: {self.__service['id']}"
        )
        logging.info('Successfully unregistered application!')

        self.__discovery.agent.service.deregister(self.__service['id'])

    def register(self,
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
            self.__create_service(service_name,
                                  service_port,
                                  healthcheck_path)
            self.__discovery.agent.service.register(
                name=self.__service['name'],
                service_id=self.__service['id'],
                check=self.__service['healthcheck'],
                address=self.__service['application_ip'],
                port=self.__service['port']
            )

            self.__id = self.get_leader_current_id()

            logging.info('Service successfully registered!')
            logging.debug(f'Consul ID: {self.__id}')

        except requests.exceptions.ConnectionError:
            logging.error("Failed to connect to discovery...")
