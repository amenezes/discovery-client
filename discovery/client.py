"""Consul discovery client module."""

import logging
import time

import consul

from discovery.base_client import BaseClient
from discovery.check import Check
from discovery.filter import Filter
from discovery.utils import select_one_rr

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

        self.__discovery.agent.service.deregister(service.identifier)
        self.__discovery.agent.service.register(
            name=service.name,
            service_id=service.identifier,
            check=service.check,
            address=service.ip,
            port=service.port)
        self.__id = self.leader_current_id()
        logging.info('Service successfully re-registered')

    def leader_current_id(self):
        """Retrieve current ID from consul leader."""
        consul_leader = self.__discovery.status.leader()
        consul_instances = self.__discovery.health.service('consul')[Filter.PAYLOAD.value]
        current_id = [instance['Node']['ID']
                      for instance in consul_instances
                      if instance['Node']['Address'] == consul_leader.split(':')[Filter.FIRST_ITEM.value]]

        if len(current_id) > 0:
            current_id = current_id[Filter.FIRST_ITEM.value]

        return current_id[Filter.FIRST_ITEM.value]

    def check_consul_health(self, service):
        """Start a loop that check consul health.

        Necessary to re-register service in case of consul fail.
        """
        while True:
            try:
                time.sleep(self.DEFAULT_TIMEOUT)

                current_id = self.leader_current_id()
                logging.debug(f"Consul ID: {current_id}")

                if current_id != self.__id:
                    self.__reconnect(service)

            except requests.exceptions.ConnectionError:
                logging.error("Failed to connect to discovery service...")
                logging.error(
                    f'Reconnect will occur in {self.DEFAULT_TIMEOUT} seconds.'
                )

    def find_service(self, name, fn=select_one_rr):
        """Search for a service in the consul's catalog."""
        return fn(self.find_services(name))

    def find_services(self, name):
        """
        Search for a service in the consul's catalog.

        Return a list of services registered on consul catalog.
        """
        services = self.__discovery.catalog.service(name)
        return self._format_catalog_service(services)

    def deregister(self, service_id):
        """Deregister a service registered.

        Keyword arguments:
        service_id -- a valid service_id from a service previously registered.
        """
        logging.debug(
            f"Unregistering service_id: {service_id}")

        self.__discovery.agent.service.deregister(service_id)

        logging.info('Successfully unregistered application!')

    def register(self, service):
        """Register a new service."""
        try:
            self.__discovery.agent.service.register(
                name=service.name,
                service_id=service.identifier,
                check=service.check,
                address=service.ip,
                port=service.port)
            self.__id = self.leader_current_id()

            logging.info('Service successfully registered!')
            logging.debug(f'Consul ID: {self.__id}')

        except requests.exceptions.ConnectionError:
            logging.error("Failed to connect to discovery...")

    def register_additional_check(self, check, service_id):
        """Append a Consul's check to a service registered."""
        if isinstance(check, Check):
            self.__discovery.agent.check.register(
                check.name, check.value, service_id=service_id)
        else:
            raise TypeError('check must be Check instance.')

    def register_additional_checks(self, service):
        """Append a Consul's check to a service registered."""
        for check in service.additional_checks():
            self.register_additional_check(check, service.identifier)

    def deregister_additional_check(self, check_id):
        """Remove a Consul's check to a service registered."""
        self.__discovery.agent.check.deregister(check_id)

    def deregister_additional_checks(self, service):
        """Remove a Consul's check to a service registered."""
        for check in service.additional_checks():
            self.deregister_additional_check(check.identifier)
