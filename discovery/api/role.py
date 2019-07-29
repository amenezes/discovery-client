import attr

from discovery.api.base import BaseApi


@attr.s(frozen=True, slots=True)
class Role(BaseApi):
    endpoint = attr.ib(default='/acl/role')

    def create(self, data, **kwargs):
        return self.client.put(f"{self.url}", params=kwargs, data=data)

    def read(self, role_id, **kwargs):
        return self.client.put(f"{self.url}/{role_id}", params=kwargs)

    def read_by_name(self, name, **kwargs):
        return self.client.put(f"{self.url}/name/{name}", params=kwargs)

    def update(self, role_id, **kwargs):
        return self.client.put(f"{self.url}/{role_id}", params=kwargs)

    def delete(self, role_id, **kwargs):
        return self.client.delete(f"{self.url}/{role_id}", params=kwargs)

    def list(self, **kwargs):
        return self.client.get(f"{self.url}s", params=kwargs)
