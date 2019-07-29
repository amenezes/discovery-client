import attr

from discovery.api.base import BaseApi


@attr.s(frozen=True, slots=True)
class Segment(BaseApi):
    endpoint = attr.ib(default='/operator/segment')

    def list(self, **kwargs):
        return self.client.get(f"{self.url}", params=kwargs)
