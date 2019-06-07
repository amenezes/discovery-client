"""Consul check module."""

import uuid


class Check:
    """Consul healthcheck."""

    def __init__(self, name):
        """Create a instance for consul's check."""
        self.__definition = dict()
        self.__definition['name'] = name
        self.__definition['id'] = f"{uuid.uuid4().hex}"

    def __str__(self):
        """Override default __str__ to represent current Check."""
        return str(self.__definition)

    @property
    def name(self):
        """Name check getter."""
        return self.__definition['name']

    @property
    def id(self):
        """Id check getter."""
        return self.__definition['id']

    def tcp(self, tcp, interval='10s', timeout='5s'):
        """Configure a TCP healthcheck."""
        self.__definition['tcp'] = tcp
        self.__definition['interval'] = interval
        self.__definition['timeout'] = timeout

    def http(self, url, interval='10s', timeout='5s'):
        """Configure a HTTP healthcheck."""
        self.__definition['http'] = url
        self.__definition['interval'] = interval
        self.__definition['timeout'] = timeout

    def alias(self, alias_service):
        """Configure a check alias from a health state of another service."""
        self.__definition['alias_service'] = alias_service
