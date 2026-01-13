from enum import StrEnum, unique


@unique
class Behavior(StrEnum):
    RELEASE = "release"
    DELETE = "delete"
