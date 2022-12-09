from dataclasses import dataclass


@dataclass
class ACLLink:
    uuid: str
    name: str


@dataclass
class PolicyDefaults(ACLLink):
    pass


@dataclass
class RoleDefaults(ACLLink):
    pass
