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

    def __init__(self,
                 name,
                 port,
                 ip='',
                 identifier='',
                 node='',
                 node_id='',
                 check=None):
        """Create a instance for consul's service."""
        self._name = name
        self._port = port
        self._ip = ip
        self._identifier = identifier
        self._node = node
        self._node_id = node_id

        if ip == '':
            self._ip = socket.gethostbyname(socket.gethostname())

        if identifier == '':
            self._identifier = f"{name}-{uuid.uuid4().hex}"

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
    def identifier(self):
        """Getter from id property."""
        return self._identifier

    @property
    def node(self):
        return self._node

    @property
    def node_id(self):
        return self._node_id

    @property
    def check(self):
        """Getter from healthcheck property."""
        response = {}
        if self._check:
            response = self._check.value
        return response
    
    @property
    def raw(self):
        """Return Service instance as dict."""
        return {
            'node': self._node,
            'node_id': self._node_id,
            'address': self._ip,
            'service_id': self._identifier,
            'service_name': self._name,
            'service_port': self._port
        }

    def append(self, check):
        """Append an additional Consul's check to a service registered.

        Keyword arguments:
        check -- additional check instance to append on service.
        """
        if isinstance(check, Check):
            self._additional_checks.update({check.name: check})
        else:
            raise TypeError('check must be Check instance')

    def remove(self, check_name):
        """Remove an additional Consul's check to a service registered.

        Keyword arguments:
        name -- additional check name.
        """
        if check_name in self._additional_checks.keys():
            self._additional_checks.pop(check_name)
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
        return str(f"Service:{id(self)} name: {self.name}, port: {self.port}, id: {self.identifier}, ip: {self.ip}, healthcheck: {self.check})")
