import attr

from discovery.api.base import BaseApi


@attr.s(frozen=True, slots=True)
class CA(BaseApi):
    endpoint = attr.ib(default='/connect/ca')

    def list(self):
        return self.client.get(f"{self.url}/roots")

    def configuration(self):
        return self.client.get(f"{self.url}/configuration")

    def update(self, data):
        return self.client.put(f"{self.url}/configuration", data=data)
