from enum import StrEnum, unique


@unique
class TokenLocality(StrEnum):
    LOCAL = "local"
    GLOBAL = "global"
