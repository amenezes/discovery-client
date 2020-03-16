import abc
import os

from discovery import api


class BaseClient(abc.ABC):
    def __init__(self, client, timeout=30, **kwargs):
        self.client = client or api.AioEngine()
        self._timeout = int(os.getenv("DEFAULT_TIMEOUT", timeout))

        # base api
        self.catalog = kwargs.get("catalog") or api.Catalog(client=client)
        self.config = kwargs.get("config") or api.Config(client=client)
        self.coordinate = kwargs.get("coordinate") or api.Coordinate(client=client)
        self.events = kwargs.get("events") or api.Events(client=client)
        self.health = kwargs.get("health") or api.Health(client=client)
        self.kv = kwargs.get("kv") or api.Kv(client=client)
        self.query = kwargs.get("query") or api.Query(client=client)
        self.session = kwargs.get("session") or api.Session(client=client)
        self.snapshot = kwargs.get("snapshot") or api.Snapshot(client=client)
        self.status = kwargs.get("status") or api.Status(client=client)
        self.txn = kwargs.get("txn") or api.Txn(client=client)
        # agent
        self.agent = kwargs.get("agent") or api.Agent(client=client)
        # connect
        self.connect = kwargs.get("connect") or api.Connect(client=client)
        # acl
        self.acl = kwargs.get("acl") or api.Acl(client=client)
        # operator
        self.operator = kwargs.get("operator") or api.Operator(client=client)

    @property
    def timeout(self):
        return self._timeout

