"""Consul discovery base client module."""

import logging
import os
from abc import ABC

import attr

from discovery.api.acl import Acl
from discovery.api.agent import Agent
from discovery.api.catalog import Catalog
from discovery.api.config import Config
from discovery.api.coordinate import Coordinate
from discovery.api.events import Events
from discovery.api.health import Health
from discovery.api.kv import Kv
from discovery.api.operator import Operator
from discovery.api.query import Query
from discovery.api.session import Session
from discovery.api.snapshot import Snapshot
from discovery.api.status import Status
from discovery.api.txn import Txn
from discovery.core.engine.base import Engine
from discovery.core.engine.standard import StandardEngine
from discovery.filter import Filter


logging.getLogger(__name__).addHandler(logging.NullHandler())


@attr.s(slots=True)
class BaseClient(ABC):
    """Consul Base Client."""

    # __id = ''
    _id = attr.ib(type=str, default='')
    client = attr.ib(
        type=Engine,
        default=StandardEngine(),
        validator=attr.validators.instance_of(Engine)
    )
    _timeout = attr.ib(
        type=int,
        default=os.getenv('DEFAULT_TIMEOUT'),
        converter=attr.converters.default_if_none(
            Filter.DEFAULT_TIMEOUT.value
        )
    )
    acl = attr.ib(type=Acl, default=None)
    agent = attr.ib(type=Agent, default=None)
    catalog = attr.ib(type=Catalog, default=None)
    config = attr.ib(type=Config, default=None)
    coordinate = attr.ib(type=Coordinate, default=None)
    events = attr.ib(type=Events, default=None)
    health = attr.ib(type=Health, default=None)
    kv = attr.ib(type=Kv, default=None)
    operator = attr.ib(type=Operator, default=None)
    query = attr.ib(type=Query, default=None)
    session = attr.ib(type=Session, default=None)
    snapshot = attr.ib(type=Snapshot, default=None)
    status = attr.ib(type=Status, default=None)
    txn = attr.ib(type=Txn, default=None)

    def __attrs_post_init__(self):
        self.acl = Acl(self.client)
        self.agent = Agent(self.client)
        self.catalog = Catalog(self.client)
        self.config = Config(self.client)
        self.coordinate = Coordinate(self.client)
        self.events = Events(self.client)
        self.health = Health(self.client)
        self.kv = Kv(self.client)
        self.operator = Operator(self.client)
        self.query = Query(self.client)
        self.session = Session(self.client)
        self.snapshot = Snapshot(self.client)
        self.status = Status(self.client)
        self.txn = Txn(self.client)

    @property
    def timeout(self):
        return int(self._timeout)
