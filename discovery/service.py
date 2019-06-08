"""Consul service module."""

import logging
import socket
import uuid

logging.getLogger(__name__).addHandler(logging.NullHandler())


class Service:
    """Consul service."""

    __healthcheck = {}

    def __init__(self, name, port, check=None):
        """Create a instance for consul's service."""
        self.__name = name
        self.__port = port
        self.__id = f"{name}-{uuid.uuid4().hex}"
        self.__ip = socket.gethostbyname(socket.gethostname())

        if check:
            self.__healthcheck = str(check)

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
        return str(self.__healthcheck)
