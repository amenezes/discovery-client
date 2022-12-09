from enum import Enum, unique


@unique
class IntentionBy(str, Enum):
    NAME: str = "name"
    SOURCE: str = "source"
    DESTINATION: str = "destination"

    def __str__(self):
        return str.__str__(self)
