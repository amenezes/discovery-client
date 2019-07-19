"""Consul check module."""

import uuid

import attr


@attr.s
class Check:
    """Consul healthcheck."""

    _value = {}
    _name = attr.ib(
        type=str,
        validator=attr.validators.optional(
            attr.validators.instance_of(str)
        )
    )
    _check = attr.ib(
        validator=attr.validators.instance_of(dict)
    )
    _identifier = attr.ib(
        default="{uuid}",
        validator=attr.validators.optional(
            attr.validators.instance_of(str)
        )
    )

    def __attrs_post_init__(self):
        self._identifier = self._identifier.format(
            uuid=uuid.uuid4().hex
        )
        self._value.update({'name': self._name})
        self._value.update({'id': self._identifier})
        self._value.update(self._check)

    @property
    def value(self):
        """Check object getter."""
        return self._value

    @property
    def name(self):
        """Name check getter."""
        return self._name

    @property
    def identifier(self):
        """Id check getter."""
        return self._identifier


def tcp(tcp, interval='10s', timeout='5s'):
    """Configure a TCP healthcheck.

    Keyword arguments:
    url -- TCP endpoint
    interval -- interval check (default '10s')
    timeout -- timeout (default '5s')
    """
    return {'tcp': tcp, 'interval': interval, 'timeout': timeout}


def http(url, interval='10s', timeout='5s', deregister_after='1m'):
    """Configure a HTTP healthcheck.

    Keyword arguments:
    url -- endpoint URL
    interval -- interval check (default '10s')
    timeout -- timeout (default '5s')
    """
    return {
        'http': url,
        'interval': interval,
        'timeout': timeout,
        'DeregisterCriticalServiceAfter': deregister_after
    }


def alias(alias_service):
    """Configure a check alias from a health state of another service.

    Keyword arguments:
    alias_service -- service registered on Consul's catalog.
    """
    return {'alias_service': alias_service}
