"""Consul discovery client module."""

import logging
import time

import consul

from discovery.consul.base_client import BaseClient
from discovery.consul.filter import Filter
from discovery.consul.utils import select_one_randomly, select_one_rr

import requests


logging.getLogger(__name__).addHandler(logging.NullHandler())


class Consul(BaseClient):
    """Consul Service Registry."""

    def __init__(self, host='localhost', port=8500):
        """Create a instance for standard consul client."""
        super().__init__()
        self.__discovery = consul.Consul(host, port)

    def __reconnect(self, service):
        """Service re-registration steps."""
        logging.debug('Service reconnect fallback')

        self.__discovery.agent.service.deregister(service.id)
        self.__discovery.agent.service.register(
            name=service.name,
            service_id=service.id,
            check=service.healthcheck,
            address=service.ip,
            port=service.port
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

    def check_consul_health(self, service):
        """Start a loop that check consul health.

        Necessary to re-register service in case of consul fail.
        """
        while True:
            try:
                time.sleep(self.DEFAULT_TIMEOUT)

                current_id = self.get_leader_current_id()
                logging.debug(f"Consul ID: {current_id}")

                if current_id != self.__id:
                    self.__reconnect(service)

            except requests.exceptions.ConnectionError:
                logging.error("Failed to connect to discovery service...")
                logging.error(
                    f'Reconnect will occur in {self.DEFAULT_TIMEOUT} seconds.'
                )

    def find_service(self, name, method='rr'):
        """Search for a service in the consul's catalog.

        Return a specific service using: round robin (default) or random.
        """
        services = self.find_services(name)

        if method == 'rr':
            service = select_one_rr(name, services)
        else:
            service = select_one_randomly(services)
        return service

    def find_services(self, name):
        """
        Search for a service in the consul's catalog.

        Return a list of services registered on consul catalog.
        """
        services = self.__discovery.catalog.service(name)
        return self._format_catalog_service(services)

    def deregister(self, service):
        """Deregister a service registered."""
        logging.debug(
            f"Unregistering service id: {service.id}"
        )
        logging.info('Successfully unregistered application!')

        self.__discovery.agent.service.deregister(service.id)

    def register(self, service):
        """Register a new service."""
        try:
            self.__discovery.agent.service.register(
                name=service.name,
                service_id=service.id,
                check=service.healthcheck,
                address=service.ip,
                port=service.port
            )

            self.__id = self.get_leader_current_id()

            logging.info('Service successfully registered!')
            logging.debug(f'Consul ID: {self.__id}')

        except requests.exceptions.ConnectionError:
            logging.error("Failed to connect to discovery...")

    # def filter_by_status(self, service, status):
    #     response = []
    #     raw_response = self.__discovery.health.service(service)
    #     for service in raw_response[Filter.PAYLOAD.value]:
    #         for status in service['Checks']:
    #             if status['passing']:
    #                 response.append(service)
    #     return response

    def register_service_dependency_healthcheck(self, service, check):
        """Append a healthcheck to a service registered."""
        self.__discovery.agent.check.register(
            check.name, check.value, service_id=service.id)

    def deregister_service_dependency_healthcheck(self, service, check):
        """Remove a healthcheck to a service registered."""
        self.__discovery.agent.check.deregister(check.id)
