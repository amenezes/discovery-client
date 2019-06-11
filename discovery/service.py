"""Consul service module."""

import logging
import socket
import uuid

from discovery.check import Check


logging.getLogger(__name__).addHandler(logging.NullHandler())


class Service:
    """Consul service."""

    _check = None
    _additional_checks = {}

    def __init__(self, name, port, check=None):
        """Create a instance for consul's service."""
        self._name = name
        self._port = port
        self._id = f"{name}-{uuid.uuid4().hex}"
        self._ip = socket.gethostbyname(socket.gethostname())

        if isinstance(check, Check):
            self._check = check

    @property
    def name(self):
        """Getter from name property."""
        return self._name

    @property
    def port(self):
        """Getter from port property."""
        return self._port

    @property
    def ip(self):
        """Getter from ip property."""
        return self._ip

    @property
    def id(self):
        """Getter from id property."""
        return self._id

    @property
    def check(self):
        """Getter from healthcheck property."""
        response = {}
        if self._check:
            response = self._check.value
        return response

    def append_check(self, check):
        """Append an additional Consul's check to a service registered.

        Keyword arguments:
        check -- additional check instance to append on service.
        """
        if isinstance(check, Check):
            self._additional_checks.update({check.name: check})
        else:
            raise TypeError('check must be Check instance')

    def remove_check(self, name):
        """Remove an additional Consul's check to a service registered.

        Keyword arguments:
        name -- additional check name.
        """
        if name in self._additional_checks.keys():
            self._additional_checks.pop(name)
        else:
            raise ValueError('check not previously registered.')

    def additional_checks(self):
        """Retrieve all additional checks from a service."""
        return [check for check in self._additional_checks.values()]

    def additional_check(self, name):
        """Retrieve a specific additional check from a service."""
        if name in self._additional_checks.keys():
            return self._additional_checks.get(name)
        else:
            raise ValueError('check not previously registered.')

    def __str__(self):
        """Representation of Service object."""
        return str(f"Service:{id(self)} name: {self.name}, port: {self.port}, id: {self.id}, ip: {self.ip}, healthcheck: {self.check})")
