"""Consul discovery base client module."""

import logging
import os
from abc import ABC

from discovery.filter import Filter
from discovery.service import Service


logging.getLogger(__name__).addHandler(logging.NullHandler())


class BaseClient(ABC):
    """Consul Base Client."""

    __id = ''
    DEFAULT_TIMEOUT = int(Filter.DEFAULT_TIMEOUT.value)

    def __init__(self):
        """Create a instance for standard consul client."""
        if os.getenv('DEFAULT_TIMEOUT'):
            self.DEFAULT_TIMEOUT = int(os.getenv('DEFAULT_TIMEOUT'))

    def _format_catalog_service(self, services):
        return [Service(
            svc['ServiceName'],
            svc['ServicePort'],
            ip=svc['Address'],
            identifier=svc['ServiceID'],
            node=svc['Node'],
            node_id=svc['ID'])
            for svc in services[Filter.PAYLOAD.value]]
