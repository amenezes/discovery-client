import asyncio

import graphene

from discovery import log
from discovery.client import Consul

# import pdb


loop = asyncio.get_event_loop()
discovery = Consul()


def log_middleware(next, root, info, **kwargs):
    # pdb.set_trace()
    log.info(">> log_middleware")
    response = next(root, info, **kwargs)
    return response


class ConfigKind(graphene.Enum):
    Service = "service-defaults"
    Proxy = "proxy-defaults"


class ServiceInterface(graphene.Interface):
    service = graphene.JSONString()


class NodeInterface(graphene.Interface):
    node = graphene.String()


class ConfigInput(graphene.InputObjectType):
    kind = ConfigKind(required=True)
    name = graphene.String(required=True)


class AclGraph(graphene.ObjectType):
    replication = graphene.JSONString()

    def resolve_replication(self, info):
        return loop.run_until_complete(discovery.acl.replication())


class ConfigGraph(graphene.ObjectType):
    list = graphene.List(graphene.JSONString)

    def resolve_list(self, info):
        return loop.run_until_complete(discovery.config.list(self.list)).json()


class AgentGraph(graphene.ObjectType):
    members = graphene.String()
    configuration = graphene.String()
    metrics = graphene.String()

    def resolve_members(self, info):
        return loop.run_until_complete(discovery.agent.metrics()).json()

    def resolve_configuration(self, info):
        return loop.run_until_complete(discovery.agent.read_configuration()).json()

    def resolve_metrics(self, info):
        return loop.run_until_complete(discovery.agent.metrics()).json()


class CatalogGraph(graphene.ObjectType):
    class Meta:
        interfaces = (
            ServiceInterface,
            NodeInterface,
        )

    datacenters = graphene.List(graphene.String)
    nodes = graphene.JSONString()
    services = graphene.JSONString()

    def resolve_datacenters(self, info):
        return loop.run_until_complete(discovery.catalog.datacenters()).json()

    def resolve_nodes(self, info):
        return loop.run_until_complete(discovery.catalog.nodes()).json()

    def resolve_services(self, info):
        return loop.run_until_complete(discovery.catalog.services()).json()

    def resolve_service(self, info):
        return loop.run_until_complete(discovery.catalog.service(self.service)).json()

    def resolve_node(self, info):
        return loop.run_until_complete(discovery.catalog.node(self.node)).json()


class RaftGraph(graphene.ObjectType):
    configuration = graphene.JSONString()

    def resolve_configuration(self, info):
        return loop.run_until_complete(
            discovery.operator.raft.read_configuration()
        ).json()


class StatusGraph(graphene.ObjectType):
    leader = graphene.String()
    peers = graphene.List(graphene.String)

    def resolve_leader(self, info):
        return loop.run_until_complete(discovery.status.leader()).json()

    def resolve_peers(self, info):
        return loop.run_until_complete(discovery.status.peers()).json()


class HealthGraph(graphene.ObjectType):
    class Meta:
        interfaces = (
            ServiceInterface,
            NodeInterface,
        )

    checks = graphene.JSONString()
    state = graphene.JSONString()

    def resolve_checks(self, info):
        return loop.run_until_complete(discovery.health.checks(self.checks)).json()

    def resolve_node(self, info):
        return loop.run_until_complete(discovery.health.node(self.node)).json()

    def resolve_service(self, info):
        return loop.run_until_complete(discovery.health.service(self.service)).json()

    def resolve_state(self, info):
        return loop.run_until_complete(discovery.health.state(self.state)).json()


class Query(graphene.ObjectType):
    acl = graphene.Field(AclGraph)
    agent = graphene.Field(AgentGraph)
    catalog = graphene.Field(
        CatalogGraph,
        service=graphene.String(default_value="consul"),
        node=graphene.String(default_value="localhost"),
    )
    status = graphene.Field(StatusGraph)
    raft = graphene.Field(RaftGraph)
    health = graphene.Field(
        HealthGraph,
        service=graphene.String(default_value="consul"),
        state=graphene.String(default_value="passing"),
        node=graphene.String(default_value="localhost"),
    )
    config = graphene.Field(ConfigGraph, list=ConfigKind())

    def resolve_acl(root, info):
        return AclGraph()

    def resolve_agent(root, info):
        return AgentGraph()

    def resolve_catalog(root, info, service, node):
        return CatalogGraph(service=service, node=node)

    def resolve_raft(root, info):
        return RaftGraph()

    def resolve_status(root, info):
        return StatusGraph()

    def resolve_health(root, info, service, state, node):
        return HealthGraph(checks=service, node=node, service=service, state=state)

    def resolve_config(root, info, list):
        return ConfigGraph(list=list)


schema = graphene.Schema(query=Query)


def execute(query):
    query_fmt = f"query { {query} }"
    log.debug(query_fmt.replace("'", ""))
    return schema.execute(query_fmt.replace("'", ""), middleware=[log_middleware]).data
