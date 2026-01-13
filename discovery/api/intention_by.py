from enum import StrEnum, unique


@unique
class IntentionBy(StrEnum):
    NAME = "name"
    SOURCE = "source"
    DESTINATION = "destination"
