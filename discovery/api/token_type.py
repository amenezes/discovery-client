from enum import Enum, unique


@unique
class TokenType(str, Enum):
    DEFAULT: str = "default"
    AGENT: str = "agent"
    AGENT_RECOVERY: str = "agent_recovery"
    REPLICATION: str = "replication"
    AGENT_MASTER: str = "agent_master"
    ACL_TOKEN: str = "acl_token"
    ACL_AGENT_TOKEN: str = "acl_agent_token"
    ACL_AGENT_MASTER_TOKEN: str = "acl_agent_master_token"
    ACL_REPLICATION_TOKEN: str = "acl_replication_token"

    def __str__(self):
        return str.__str__(self)
