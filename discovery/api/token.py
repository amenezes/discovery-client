import attr

from discovery.api.base import BaseApi


@attr.s(frozen=True, slots=True)
class Token(BaseApi):
    endpoint = attr.ib(default='/acl/token')

    def create(self):
        return self.client.put(f"{self.url}")

    def read(self):
        pass

    def read_self(self):
        pass

    def update(self):
        pass

    def clone(self):
        pass

    def delete(self):
        pass

    def list(self):
        pass
