import attr

from discovery.api.base import BaseApi


@attr.s(frozen=True, slots=True)
class Raft(BaseApi):
    endpoint = attr.ib(default='/operator/raft')

    def read_configuration(self, **kwargs):
        return self.client.get(f"{self.url}/configuration", params=kwargs)

    def delete_peer(self, **kwargs):
        print(kwargs)
        return self.client.delete(
            f"{self.url}/peer", params=kwargs
        )
