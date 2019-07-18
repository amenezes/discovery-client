"""Consul service module."""

import logging
import socket
import uuid

import attr

from discovery.check import Check


logging.getLogger(__name__).addHandler(logging.NullHandler())


@attr.s
class Service:
    """Consul service."""

    _checks = {}
    name = attr.ib()
    port = attr.ib()
    node = attr.ib(default='')
    node_id = attr.ib(default='')
    _check = attr.ib(
        default=None,
        validator=attr.validators.optional(
            attr.validators.instance_of(Check)
        )
    )
    ip = attr.ib(
        default=None,
        converter=attr.converters.default_if_none(
            socket.gethostbyname(socket.gethostname())
        )
    )
    identifier = attr.ib(
        default="{name}-{uuid}"
    )

    def __attrs_post_init__(self):
        self.identifier = self.identifier.format(
            name=self.name,
            uuid=uuid.uuid4().hex
        )
        if self._check is not None:
            self._checks.update({self._check.name: self._check})

    @property
    def check(self):
        return self._check

    @check.setter
    def check(self, value):
        if not isinstance(value, Check):
            raise TypeError('check must be instance of Check.')
        self._check = value
        self._checks.update({self._check.name: self._check})

    @property
    def raw(self):
        """Return Service instance as dict."""
        return {
            'node': self.node,
            'node_id': self.node_id,
            'address': self.ip,
            'service_id': self.identifier,
            'service_name': self.name,
            'service_port': self.port
        }

    def append(self, check):
        """Append an additional Consul's check to a service registered.

        Keyword arguments:
        check -- additional check instance to append on service.
        """
        if not isinstance(check, Check):
            raise TypeError('check must be Check instance')
        self._checks.update({check.name: check})

    def remove(self, check_name):
        """Remove an additional Consul's check to a service registered.

        Keyword arguments:
        name -- additional check name.
        """
        if check_name not in self._checks.keys():
            raise ValueError('check not previously registered.')
        elif check_name == self._check.name:
            self._check = None
        self._checks.pop(check_name)

    def list_checks(self):
        """Retrieve all additional checks from a service."""
        return [check for check in self._checks.values()]
        t = None
        for check in self._checks.values():
            t.append(check)

    def get_check(self, name):
        """Retrieve a specific additional check from a service."""
        if name not in self._checks.keys():
            raise ValueError('check not previously registered.')
        return self._checks.get(name)
