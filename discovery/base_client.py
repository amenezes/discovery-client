"""Consul discovery base client module."""
import logging
import os
from abc import ABC

from discovery.filter import Filter


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
        return [{"node": svc['Node'],
                 "node_id": svc['ID'],
                 "address": svc['Address'],
                 "service_id": svc['ServiceID'],
                 "service_name": svc['ServiceName'],
                 "service_port": svc['ServicePort']}
                for svc in services[Filter.PAYLOAD.value]]
