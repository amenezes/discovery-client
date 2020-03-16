from discovery import api
from discovery.api.abc import Api


class Connect(Api):
    def __init__(
        self, ca=None, intentions=None, endpoint: str = "/agent/connect", **kwargs
    ):
        super().__init__(endpoint=endpoint, **kwargs)
        self.ca = ca or api.CA(client=self.client)
        self.intentions = intentions or api.Intentions(client=self.client)
