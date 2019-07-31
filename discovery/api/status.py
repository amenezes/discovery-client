import attr

from discovery.api.base import BaseApi


@attr.s(frozen=True, slots=True)
class Status(BaseApi):
    endpoint = attr.ib(default='/status')

    def leader(self, **kwargs):
        return self.client.get(f"{self.url}/leader", params=kwargs)

    def peers(self, **kwargs):
        return self.client.get(f"{self.url}/peers", params=kwargs)
