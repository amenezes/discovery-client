from enum import StrEnum, unique


@unique
class IntentionFilter(StrEnum):
    ACTION = "Action"
    DESCRIPTION = "Description"
    DESTINATION_NS = "DestinationNS"
    DESTINATION_NAME = "DestinationName"
    ID = "ID"
    META = "Meta"
    META_ANY = "Meta.<any>"
    PRECEDENCE = "Precedence"
    SOURCE_NS = "SourceNS"
    SOURCE_NAME = "SourceName"
    SOURCE_TYPE = "SourceType"
