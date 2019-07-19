"""Consul discovery base client module."""

import logging
import os
from abc import ABC

from discovery.filter import Filter
from discovery.service import Service

import attr


logging.getLogger(__name__).addHandler(logging.NullHandler())


@attr.s
class BaseClient(ABC):
    """Consul Base Client."""

    __id = ''
    _timeout = attr.ib(
        default=os.getenv('DEFAULT_TIMEOUT'),
        converter=attr.converters.default_if_none(
            int(Filter.DEFAULT_TIMEOUT.value)
        )
    )

    @property
    def timeout(self):
        return int(self._timeout)

    @timeout.setter
    def timeout(self, value):
        self._timeout = int(value)

    def _format_catalog_service(self, services):
        return [
            Service(
                name=svc.get('ServiceName'),
                port=svc.get('ServicePort'),
                ip=svc.get('Address'),
                identifier=svc.get('ServiceID'),
                node=svc.get('Node'),
                node_id=svc.get('ID'))
            for svc in services[Filter.PAYLOAD.value]
        ]
