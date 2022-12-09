from enum import Enum, unique


@unique
class IntentionsAction(str, Enum):
    ALLOW: str = "allow"
    DENY: str = "deny"

    def __str__(self):
        return str.__str__(self)
