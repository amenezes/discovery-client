"""Consul check module."""
import uuid


class Check:
    """Consul healthcheck."""

    __definition = {}

    def __init__(self, name):
        self.__name = name

    def __str__(self):
        return str(self.__definition)

    def tcp(self, tcp, interval='10s', timeout='5s'):
        self.__definition = {
            'id': f"{self.__name}-{uuid.uuid4().hex}",
            'name': self.__name,
            'tcp': tcp,
            'interval': interval,
            'timeout': timeout
        }

    def http(self, url, interval='10s', timeout='5s'):
        self.__definition = {
            'id': f"{self.__name}-{uuid.uuid4().hex}",
            'name': self.__name,
            'http': url,
            'interval': interval,
            'timeout': timeout

        }

    def alias(self, alias_service):
        self.__definition = {
            'id': f"{self.__name}-{uuid.uuid4().hex}",
            'alias_service': alias_service
        }
