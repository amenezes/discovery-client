import attr

from discovery.api.base import BaseApi


@attr.s(frozen=True, slots=True)
class Session(BaseApi):
    endpoint = attr.ib(default='/session')

    def create(self, params, **kwargs):
        return self.client.put(
            f"{self.url}/create", params=kwargs, data=kwargs
        )

    def delete(self, uuid, **kwargs):
        return self.client.put(f"{self.url}/destroy/{uuid}", params=kwargs)

    def read(self, uuid, **kwargs):
        return self.client.get(f"{self.url}/info/{uuid}", params=kwargs)

    def list_node_session(self, node, **kwargs):
        return self.client.get(f"{self.url}/node/{node}", params=kwargs)

    def list(self, **kwargs):
        return self.client.get(f"{self.url}/list", params=kwargs)

    def renew(self, uuid, **kwargs):
        return self.client.put(f"{self.url}/renew/{uuid}", params=kwargs)
