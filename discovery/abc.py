import abc
import os

from discovery import api


class BaseClient(abc.ABC):
    def __init__(self, client, timeout=30, **kwargs):
        self.client = client
        self._timeout = int(os.getenv("DEFAULT_TIMEOUT", timeout))

        # base api
        self.catalog = kwargs.get("catalog") or api.Catalog(client=self.client)
        self.config = kwargs.get("config") or api.Config(client=self.client)
        self.coordinate = kwargs.get("coordinate") or api.Coordinate(client=self.client)
        self.events = kwargs.get("events") or api.Events(client=self.client)
        self.health = kwargs.get("health") or api.Health(client=self.client)
        self.kv = kwargs.get("kv") or api.Kv(client=self.client)
        self.query = kwargs.get("query") or api.Query(client=self.client)
        self.session = kwargs.get("session") or api.Session(client=self.client)
        self.snapshot = kwargs.get("snapshot") or api.Snapshot(client=self.client)
        self.status = kwargs.get("status") or api.Status(client=self.client)
        self.txn = kwargs.get("txn") or api.Txn(client=self.client)
        # agent
        self.agent = kwargs.get("agent") or api.Agent(client=self.client)
        # connect
        self.connect = kwargs.get("connect") or api.Connect(client=self.client)
        # acl
        self.acl = kwargs.get("acl") or api.Acl(client=self.client)
        # operator
        self.operator = kwargs.get("operator") or api.Operator(client=self.client)

    @property
    def timeout(self):
        return self._timeout
