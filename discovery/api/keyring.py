import attr

from discovery.api.base import BaseApi


@attr.s(slots=True)
class Keyring(BaseApi):
    endpoint = attr.ib(default='/operator/keyring')

    def list(self, **kwargs):
        return self.client.get(f"{self.url}", params=kwargs)

    def add(self, data, **kwargs):
        return self.client.post(f"{self.url}", data=data, params=kwargs)

    def change(self, data, **kwargs):
        return self.client.put(f"{self.url}", data=data, params=kwargs)

    def delete(self, data, **kwargs):
        return self.client.delete(f"{self.url}", data=data, params=kwargs)
