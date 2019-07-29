import attr

from discovery.api.auth_method import AuthMethod
from discovery.api.base import BaseApi
from discovery.api.binding_rule import BindingRule
from discovery.api.policy import Policy
from discovery.api.role import Role
from discovery.api.token import Token


@attr.s(slots=True)
class Acl(BaseApi):
    endpoint = attr.ib(default='/acl')
    auth_method = attr.ib(type=AuthMethod, default=None)
    binding_rule = attr.ib(type=BindingRule, default=None)
    policy = attr.ib(type=Policy, default=None)
    role = attr.ib(type=Role, default=None)
    token = attr.ib(type=Token, default=None)

    def __attrs_post_init__(self):
        self.auth_method = self.auth_method or AuthMethod(self.client)
        self.binding_rule = self.binding_rule or BindingRule(self.client)
        self.policy = self.policy or Policy(self.client)
        self.role = self.role or Role(self.client)
        self.token = self.token or Token(self.client)
