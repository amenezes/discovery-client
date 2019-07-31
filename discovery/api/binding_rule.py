import attr

from discovery.api.base import BaseApi


@attr.s(slots=True)
class BindingRule(BaseApi):
    endpoint = attr.ib(default='/acl/binding-rule')

    def create(self, data, **kwargs):
        return self.client.put(f"{self.url}", data=data, params=kwargs)

    def read(self, role_id, **kwargs):
        return self.client.get(f"{self.url}/{role_id}", params=kwargs)

    def update(self, data, role_id, **kwargs):
        return self.client.put(
            f"{self.url}/{role_id}",
            data=data,
            params=kwargs
        )

    def delete(self, role_id, **kwargs):
        return self.client.delete(f"{self.url}/{role_id}", params=kwargs)

    def list(self, **kwargs):
        return self.client.get(f"{self.url}", params=kwargs)
