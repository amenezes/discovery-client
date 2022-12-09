from enum import Enum, unique


@unique
class Behavior(str, Enum):
    RELEASE: str = "release"
    DELETE: str = "delete"

    def __str__(self):
        return str.__str__(self)
