from enum import Enum, unique


@unique
class TokenLocality(str, Enum):
    LOCAL: str = "local"
    GLOBAL: str = "global"

    def __str__(self):
        return str.__str__(self)
