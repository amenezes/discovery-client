"""Consul discovery client module."""

import logging
import time

import attr

import consul

from discovery.base_client import BaseClient
from discovery.check import Check
from discovery.filter import Filter
from discovery.service import Service
from discovery.utils import select_one_rr

import requests


logging.getLogger(__name__).addHandler(logging.NullHandler())


@attr.s(kw_only=True)
class Consul(BaseClient):
    """Consul Service Registry."""

    _host = attr.ib(type=str, default='localhost')
    _port = attr.ib(type=int, default=8500)
    service = attr.ib(type=Service, default=None)

    def __attrs_post_init__(self):
        self.connect()

    def connect(self):
        self.__discovery = consul.Consul(self._host, self._port)

    def __reconnect(self):
        """Service re-registration steps."""
        logging.debug('Service reconnect fallback')

        self.__discovery.agent.service.deregister(self.service.identifier)
        self.__discovery.agent.service.register(
            name=self.service.name,
            service_id=self.service.identifier,
            check=self.service.check,
            address=self.service.ip,
            port=self.service.port)
        self.__id = self.leader_current_id()
        logging.info('Service successfully re-registered')

    def leader_current_id(self):
        """Retrieve current ID from consul leader."""
        consul_leader = self.__discovery.status.leader()
        consul_instances = self.__discovery.health.service('consul')[Filter.PAYLOAD.value]
        current_id = [instance['Node']['ID']
                      for instance in consul_instances
                      if instance['Node']['Address'] == consul_leader.split(':')[Filter.FIRST_ITEM.value]]

        if current_id is not None:
            current_id = current_id[Filter.FIRST_ITEM.value]

        return current_id

    def check_consul_health(self, service):
        """Start a loop that check consul health.

        Necessary to re-register service in case of consul fail.
        """
        while True:
            try:
                time.sleep(self.timeout)

                current_id = self.leader_current_id()
                logging.debug(f"Consul ID: {current_id}")

                if current_id != self.__id:
                    self.__reconnect(service)

            except requests.exceptions.ConnectionError:
                logging.error("Failed to connect to discovery service...")
                logging.error(
                    f'Reconnect will occur in {self.timeout} seconds.'
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

    def deregister(self):
        """Deregister a service registered.

        Keyword arguments:
        service_id -- a valid service_id from a service previously registered.
        """
        self.__discovery.agent.service.deregister(self.service.identifier)
        logging.info('Successfully unregistered application!')

    def register(self):
        """Register a new service."""
        try:
            self.__discovery.agent.service.register(
                name=self.service.name,
                service_id=self.service.identifier,
                check=self.service.check.value,
                address=self.service.ip,
                port=self.service.port)
            self.__id = self.leader_current_id()

            logging.info('Service successfully registered!')
            logging.debug(f'Consul ID: {self.__id}')

        except requests.exceptions.ConnectionError:
            logging.error("Failed to connect to discovery...")

    def register_additional_check(self, check):
        """Append a Consul's check to a service registered."""
        if not isinstance(check, Check):
            raise TypeError('check must be Check instance.')

        self.__discovery.agent.check.register(
            check.name, check.value, service_id=self.service.identifier
        )

    def deregister_additional_check(self, check):
        """Remove a Consul's check to a service registered."""
        if not isinstance(check, Check):
            raise TypeError('check must be Check instance.')

        self.__discovery.agent.check.deregister(check.identifier)
