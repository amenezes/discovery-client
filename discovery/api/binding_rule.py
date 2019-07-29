import attr

from discovery.api.base import BaseApi


@attr.s(slots=True)
class BindingRule(BaseApi):
    endpoint = attr.ib(default='/acl/binding-rule')

    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def list(self):
        pass
