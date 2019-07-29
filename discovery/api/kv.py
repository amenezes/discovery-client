import attr

from discovery.api.base import BaseApi


@attr.s(slots=True)
class Kv(BaseApi):
    endpoint = attr.ib(default='/kv')

    def create(self, key, data, **kwargs):
        return self.update(key, data, **kwargs)

    def read(self, key, **kwargs):
        return self.client.get(f"{self.url}/{key}", params=kwargs)

    def update(self, key, data, **kwargs):
        return self.client.put(f"{self.url}/{key}", params=kwargs, data=data)

    def delete(self, key, **kwargs):
        return self.client.delete(f"{self.url}/{key}", params=kwargs)
