"""Consul check module."""
import uuid


class Check:
    """Consul healthcheck."""

    __definition = {}

    def __init__(self, name):
        """Create a instance for consul's check."""
        self.__name = name
        self.__id = f"{uuid.uuid4().hex}"

    def __str__(self):
        """Override default __str__ to represent current Check."""
        return str(self.__definition)

    @property
    def value(self):
        """Check getter."""
        return self.__definition

    @property
    def name(self):
        """Name check getter."""
        return self.__name

    @property
    def id(self):
        """Id check getter."""
        return self.__id

    def tcp(self, tcp, interval='10s', timeout='5s'):
        """Configure a TCP healthcheck."""
        self.__definition = {
            'id': self.__id,
            'name': self.__name,
            'tcp': tcp,
            'interval': interval,
            'timeout': timeout
        }

    def http(self, url, interval='10s', timeout='5s'):
        """Configure a HTTP healthcheck."""
        self.__definition = {
            'id': self.__id,
            'name': self.__name,
            'http': url,
            'interval': interval,
            'timeout': timeout

        }

    def alias(self, alias_service):
        """Configure a check alias from a health state of another service."""
        self.__definition = {
            'id': self.__id,
            'alias_service': alias_service
        }
