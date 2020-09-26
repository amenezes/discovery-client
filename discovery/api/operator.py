from discovery import api
from discovery.api.abc import Api


class Operator(Api):
    def __init__(
        self,
        area=None,
        autopilot=None,
        keyring=None,
        license=None,
        raft=None,
        segment=None,
        endpoint: str = "/operator",
        **kwargs
    ):
        super().__init__(endpoint=endpoint, **kwargs)
        self.area = area or api.Area(client=self.client)
        self.autopilot = autopilot or api.AutoPilot(client=self.client)
        self.keyring = keyring or api.Keyring(client=self.client)
        self.license = license or api.License(client=self.client)
        self.raft = raft or api.Raft(client=self.client)
        self.segment = segment or api.Segment(client=self.client)
