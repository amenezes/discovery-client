from enum import Enum, unique


@unique
class LogLevel(str, Enum):
    INFO: str = "info"
    WARNING: str = "warning"
    ERROR: str = "error"
    DEBUG: str = "debug"
    CRITICAL: str = "critical"

    def __str__(self):
        return str.__str__(self)
