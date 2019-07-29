import attr

from discovery.api.base import BaseApi


@attr.s(frozen=True, slots=True)
class AuthMethod(BaseApi):
    endpoint = attr.ib(default='/acl/auth-method')

    def create(self, data):
        return self.client.put(f"{self.url}", data=data)

    def read(self, name, **kwargs):
        return self.client.put(f"{self.url}/{name}", params=kwargs)

    def update(self, name, data, **kwargs):
        return self.client.put(
            f"{self.url}/{name}",
            params=kwargs,
            data=data
        )

    def delete(self, name, **kwargs):
        return self.client.delete(f"{self.url}/{name}", params=kwargs)

    def list(self, **kwargs):
        return self.client.put(f"{self.url}s", params=kwargs)
