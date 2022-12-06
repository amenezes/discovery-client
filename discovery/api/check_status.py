from enum import Enum, unique


@unique
class CheckStatus(str, Enum):
    PASSING: str = "passing"
    WARNING: str = "warning"
    CRITICAL: str = "critical"

    def __str__(self):
        return str.__str__(self)
