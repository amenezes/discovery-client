from enum import StrEnum, unique


@unique
class HealthState(StrEnum):
    ANY = "any"
    PASSING = "passing"
    WARNING = "warning"
    CRITICAL = "critical"
