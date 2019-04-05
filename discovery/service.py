"""Consul service module."""
import logging
import socket
import uuid

logging.getLogger(__name__).addHandler(logging.NullHandler())


class Service:
    """Consul service."""

    def __init__(self, name, port):
        """Create a instance for consul's service."""
        self.__name = name
        self.__port = port
        self.__healthcheck = {
            'http': f"http://{name}:{port}/manage/health",
            'DeregisterCriticalServiceAfter': "1m",
            'interval': '10s',
            'timeout': '5s'
        }
        self.__id = f"{name}-{uuid.uuid4().hex}"
        self.__ip = socket.gethostbyname(socket.gethostname())

    def __str__(self):
        return str({
            'name': self.name,
            'port': self.port,
            'id': self.id,
            'ip': self.ip,
            'healthcheck': self.healthcheck,
        })

    @property
    def name(self):
        """Getter from name property."""
        return self.__name

    @property
    def port(self):
        """Getter from port property."""
        return self.__port

    @property
    def ip(self):
        """Getter from ip property."""
        return self.__ip

    @property
    def id(self):
        """Getter from id property."""
        return self.__id

    @property
    def healthcheck(self):
        """Getter from healthcheck property."""
        return self.__healthcheck

    @healthcheck.setter
    def healthcheck(self, value):
        """Setter from name property."""
        if type(value) not in [dict, list]:
            logging.error('Healthcheck must be a dict or list.')
            raise TypeError(
                'Service healthcheck must be a dict or list.'
            )
        self.__healthcheck = value
