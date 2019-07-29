"""Consul discovery client module."""

import logging
import time

import attr

from discovery.base_client import BaseClient
from discovery.check import Check
from discovery.exceptions import (
    ClientOperationException,
    ServiceNotFoundException
)
from discovery.filter import Filter
from discovery.service import Service as Svc
from discovery.utils import select_one_rr

from requests.exceptions import ConnectionError


logging.getLogger(__name__).addHandler(logging.NullHandler())


@attr.s(slots=True)
class Consul(BaseClient):
    """Consul Service Registry."""

    service = attr.ib(
        type=Svc,
        default=None
    )

    def reconnect(self):
        """Service re-registration steps."""
        logging.debug('Service reconnect fallback')
        self.agent.service.deregister(self.service.identifier)
        self.agent.service.register(
            name=self.service.name,
            service_id=self.service.identifier,
            check=self.service.check,
            address=self.service.ip,
            port=self.service.port)
        self._id = self.leader_current_id()
        logging.info('Service successfully re-registered')

    def leader_current_id(self):
        """Retrieve current ID from consul leader."""
        consul_leader, _ = self.status.leader().json().split(':')
        consul_instances = self.health.service('consul').json()
        current_id = [instance['Node']['ID']
                      for instance in consul_instances
                      if instance['Node']['Address'] == consul_leader]

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

                if current_id != self._id:
                    self.reconnect(service)

            except ConnectionError:
                logging.error("Failed to connect to discovery service...")
                logging.error(
                    f'Reconnect will occur in {self.timeout} seconds.'
                )

    def find_service(self, name, fn=select_one_rr):
        """Search for a service in the consul's catalog."""
        response = self.find_services(name)
        if not response.ok:
            raise ServiceNotFoundException
        return fn(response.json())

    def find_services(self, name):
        """
        Search for a service in the consul's catalog.

        Return a list of services registered on consul catalog.
        """
        return self.catalog.service(name)

    def deregister(self):
        """Deregister a service registered."""
        self.agent.service.deregister(self.service)

    def register(self):
        """Register a new service."""
        try:
            response = self.agent.service.register(self.service.json())
            if not response.ok:
                raise ClientOperationException('Error registering service.')
            self._id = self.leader_current_id()

            logging.info('Service successfully registered!')
            logging.debug(f'Consul ID: {self._id}')

        except ConnectionError:
            logging.error("Failed to connect to discovery...")

    def register_additional_check(self, check):
        """Append a Consul's check to a service registered."""
        if not isinstance(check, Check):
            raise TypeError('check must be Check instance.')

        self.client.agent.checks.register(
            check.name, check.value, service_id=self.service.identifier
        )

    def deregister_additional_check(self, check):
        """Remove a Consul's check to a service registered."""
        if not isinstance(check, Check):
            raise TypeError('check must be Check instance.')

        self.agent.check.deregister(check.identifier)
