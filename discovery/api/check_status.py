from enum import StrEnum, unique


@unique
class CheckStatus(StrEnum):
    PASSING = "passing"
    WARNING = "warning"
    CRITICAL = "critical"
