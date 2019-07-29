import attr

from discovery.api.base import BaseApi


@attr.s(frozen=True, slots=True)
class Status(BaseApi):
    endpoint = attr.ib(default='/status')

    def leader(self):
        return self.client.get(f"{self.url}/leader")

    def peers(self):
        return self.client.get(f"{self.url}/peers")
