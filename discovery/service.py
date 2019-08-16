"""Consul service module."""

import json
import logging
import socket
import uuid

import attr

from discovery.check import Check

logging.getLogger(__name__).addHandler(logging.NullHandler())


@attr.s(slots=True)
class Service:
    """Consul service."""

    name = attr.ib(
        type=str,
        validator=attr.validators.instance_of(str)
    )
    port = attr.ib(
        type=int,
        validator=attr.validators.instance_of(int)
    )
    _check = attr.ib(
        default=None,
        type=Check,
        validator=attr.validators.optional(
            attr.validators.instance_of(Check)
        )
    )
    node = attr.ib(default='')
    node_id = attr.ib(default='')
    address = attr.ib(
        default=None,
        converter=attr.converters.default_if_none(
            socket.gethostbyname(socket.gethostname())
        )
    )
    identifier = attr.ib(
        default=None,
        converter=attr.converters.default_if_none(
            "{name}-{uuid}"
        )
    )
    _checks = attr.ib(
        type=dict,
        default={},
        validator=attr.validators.instance_of(dict)
    )

    def __attrs_post_init__(self):
        self.identifier = self.identifier.format(
            name=self.name,
            uuid=uuid.uuid4().hex
        )
        if self._check:
            self._checks.update({self._check.name: self._check})
            self._checks.update({self.name: self._check})

    @property
    def check(self):
        return self._check

    @check.setter
    def check(self, value):
        if not isinstance(value, Check):
            raise(TypeError('value must be Check instance.'))
        self._check = value

    def json(self):
        """Return Service instance as dict."""
        response = dict(
            name=self.name,
            id=self.identifier,
            address=self.address,
            port=self.port,
            node=self.node,
            node_id=self.node_id
        )
        self._check = self._check or ''
        response.update({'check': json.loads(self._check.json())})
        return json.dumps(response)

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

    def get_check(self, name):
        """Retrieve a specific additional check from a service."""
        if name not in self._checks.keys():
            raise ValueError('check not previously registered.')
        return self._checks.get(name)
