import attr

from discovery.api.base import BaseApi


@attr.s(frozen=True, slots=True)
class Query(BaseApi):
    endpoint = attr.ib(default='/query')

    def create(self, data, **kwargs):
        return self.client.post(f"{self.url}", params=kwargs, data=data)

    def read(self, uuid=None, **kwargs):
        if uuid:
            uri = f"{self.url}/{uuid}"
        else:
            uri = f"{self.url}"
        return self.client.get(uri, params=kwargs)

    def update(self, uuid, data, **kwargs):
        return self.client.put(f"{self.url}/{uuid}", params=kwargs)

    def delete(self, uuid, **kwargs):
        return self.client.delete(f"{self.url}/{uuid}", params=kwargs)

    def execute(self, uuid, **kwargs):
        return self.client.get(f"{self.url}/{uuid}/execute", params=kwargs)

    def explain(self, uuid, **kwargs):
        return self.client.get(f"{self.url}/{uuid}/explain", params=kwargs)
