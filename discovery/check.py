"""Consul check module."""

import uuid


class Check:
    """Consul healthcheck."""

    def __init__(self, name, fn):
        """Create a instance for consul's check.

        Keywords arguments:
        name -- check name.
        fn -- a valid check function: tcp, alias or http.
        """
        self._value = {}
        self._value.update({'name': name})
        self._value.update({'id': f"{uuid.uuid4().hex}"})
        self._value.update(fn)

    def __str__(self):
        """Representation of Check object."""
        return str(self._value)

    @property
    def value(self):
        """Check object getter."""
        return self._value

    @property
    def name(self):
        """Name check getter."""
        return self._value['name']

    @property
    def id(self):
        """Id check getter."""
        return self._value['id']


def tcp(tcp, interval='10s', timeout='5s'):
    """Configure a TCP healthcheck.

    Keyword arguments:
    url -- TCP endpoint
    interval -- interval check (default '10s')
    timeout -- timeout (default '5s')
    """
    return {'tcp': tcp, 'interval': interval, 'timeout': timeout}


def http(url, interval='10s', timeout='5s'):
    """Configure a HTTP healthcheck.

    Keyword arguments:
    url -- endpoint URL
    interval -- interval check (default '10s')
    timeout -- timeout (default '5s')
    """
    return {'http': url, 'interval': interval, 'timeout': timeout}


def alias(alias_service):
    """Configure a check alias from a health state of another service.

    Keyword arguments:
    alias_service -- service registered on Consul's catalog.
    """
    return {'alias_service': alias_service}
