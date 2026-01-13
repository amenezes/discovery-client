from enum import StrEnum, unique


@unique
class LogLevel(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    DEBUG = "debug"
    CRITICAL = "critical"
