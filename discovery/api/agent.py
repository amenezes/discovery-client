from urllib.parse import quote_plus

import attr

from discovery.api.base import BaseApi
from discovery.api.checks import Checks
from discovery.api.connect import Connect
from discovery.api.service import Service


@attr.s(slots=True)
class Agent(BaseApi):
    endpoint = attr.ib(default='/agent')
    checks = attr.ib(type=Checks, default=None)
    connect = attr.ib(type=Connect, default=None)
    service = attr.ib(type=Service, default=None)

    def __attrs_post_init__(self):
        self.checks = self.checks or Checks(self.client)
        self.connect = self.connect or Connect(self.client)
        self.service = self.service or Service(self.client)

    def members(self, **kwargs):
        return self.client.get(f"{self.url}/members", params=kwargs)

    def self(self, **kwargs):
        return self.client.get(f"{self.url}/self", params=kwargs)

    def reload(self, **kwargs):
        return self.client.put(f"{self.url}/reload", params=kwargs)

    def maintenance(self, enable=True, reason=None, **kwargs):
        reason = reason or ''
        return self.client.put(
            f"{self.url}/maintenance?enable={enable}&reason={quote_plus(reason)}",
            params=kwargs
        )

    def metrics(self, format=None, **kwargs):
        format = format or ''
        return self.client.get(
            f"{self.url}/metrics{format}",
            params=kwargs
        )

    def stream_logs(self, loglevel='info', **kwargs):
        return self.client.get(
            f"{self.url}/monitor?loglevel={loglevel}",
            params=kwargs
        )

    def join(self, address, **kwargs):
        return self.client.put(f"{self.url}/join/{address}", params=kwargs)

    def leave(self, **kwargs):
        return self.client.put(f"{self.url}/leave", params=kwargs)

    def force_leave(self, node, **kwargs):
        return self.client.put(
            f"{self.url}/force-leave/{node}", params=kwargs
        )
