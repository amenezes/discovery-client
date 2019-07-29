import attr

from discovery.api.base import BaseApi


@attr.s(frozen=True, slots=True)
class Snapshot(BaseApi):
    endpoint = attr.ib(default='/snapshot')

    def generate(self, **kwargs):
        return self.client.get(f"{self.url}", params=kwargs)

    def restore(self, data, **kwargs):
        return self.client.put(f"{self.url}", params=kwargs, data=data)
