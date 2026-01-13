from enum import StrEnum, unique


@unique
class TokenType(StrEnum):
    DEFAULT = "default"
    AGENT = "agent"
    AGENT_RECOVERY = "agent_recovery"
    REPLICATION = "replication"
    AGENT_MASTER = "agent_master"
    ACL_TOKEN = "acl_token"
    ACL_AGENT_TOKEN = "acl_agent_token"
    ACL_AGENT_MASTER_TOKEN = "acl_agent_master_token"
    ACL_REPLICATION_TOKEN = "acl_replication_token"
