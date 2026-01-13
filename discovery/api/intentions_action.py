from enum import StrEnum, unique


@unique
class IntentionsAction(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
