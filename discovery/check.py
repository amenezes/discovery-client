"""Consul check module."""

import json
import uuid

import attr


@attr.s(slots=True)
class Check:
    """Consul healthcheck."""

    _check = attr.ib(
        type=dict,
        validator=attr.validators.instance_of(dict)
    )
    name = attr.ib(
        type=str,
        default=None,
        converter=attr.converters.default_if_none('{name}'),
    )
    identifier = attr.ib(
        type=str,
        default=None,
        converter=attr.converters.default_if_none('{identifier}')
    )

    def __attrs_post_init__(self):
        self.name = self.name.format(name=uuid.uuid4().hex)
        self.identifier = self.identifier.format(
            identifier=uuid.uuid4().hex
        )

    def json(self):
        response = dict(id=self.identifier)
        response.update(self._check)
        return json.dumps(response)


def script(args, interval='10s', timeout='5s'):
    """Configure a Script healthcheck.

    Keyword arguments:
    args -- args
    interval -- interval check (default '10s')
    timeout -- timeout (default '5s')
    """
    return {'args': args, 'interval': interval, 'timeout': timeout}


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


def tcp(tcp, interval='10s', timeout='5s'):
    """Configure a TCP healthcheck.

    Keyword arguments:
    url -- TCP endpoint
    interval -- interval check (default '10s')
    timeout -- timeout (default '5s')
    """
    return {'tcp': tcp, 'interval': interval, 'timeout': timeout}


def ttl(self, notes, ttl='30s'):
    """Configure a TTL healthcheck.

    Keyword arguments:
    notes -- notes
    ttl -- ttl (default '30s')
    """
    return {'notes': notes, 'ttl': ttl}


def docker(container_id, args, interval='10s'):
    """Configure a Docker healthcheck.

    Keyword arguments:
    container_id -- docker_container_id
    args -- args
    interval -- interval (default '10s')
    """
    return {'docker_container_id': container_id, 'args': args, 'interval': interval}


def grpc(grpc, tls=True, interval='10s'):
    """Configure a GRPC healthcheck.

    Keyword arguments:
    grpc_address -- GRPC endpoint
    tls -- grpc_use_tls (default 'True')
    interval -- interval (default '10s')
    """
    return {'grpc': grpc, 'grpc_use_tls': tls, 'interval': interval}


def alias(alias_service):
    """Configure a check alias from a health state of another service.

    Keyword arguments:
    alias_service -- service registered on Consul's catalog.
    """
    return {'alias_service': alias_service}
