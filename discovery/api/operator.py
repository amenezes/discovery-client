import attr

from discovery.api.area import Area
from discovery.api.autopilot import AutoPilot
from discovery.api.base import BaseApi
from discovery.api.keyring import Keyring
from discovery.api.license import License
from discovery.api.raft import Raft
from discovery.api.segment import Segment


@attr.s(slots=True)
class Operator(BaseApi):
    area = attr.ib(type=Area, default=None)
    autopilot = attr.ib(type=AutoPilot, default=None)
    keyring = attr.ib(type=Keyring, default=None)
    license = attr.ib(type=License, default=None)
    raft = attr.ib(type=Raft, default=None)
    segment = attr.ib(type=Segment, default=None)

    def __attrs_post_init__(self):
        self.area = Area(self.client)
        self.autopilot = AutoPilot(self.client)
        self.keyring = Keyring(self.client)
        self.license = License(self.client)
        self.raft = Raft(self.client)
        self.segment = Segment(self.client)
