from enum import Enum, unique


@unique
class HealthState(str, Enum):
    ANY: str = "any"
    PASSING: str = "passing"
    WARNING: str = "warning"
    CRITICAL: str = "critical"

    def __str__(self):
        return str.__str__(self)
