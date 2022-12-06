from enum import Enum, unique


@unique
class IntentionFilter(str, Enum):
    ACTION: str = "Action"
    DESCRIPTION: str = "Description"
    DESTINATION_NS: str = "DestinationNS"
    DESTINATION_NAME: str = "DestinationName"
    ID: str = "ID"
    META: str = "Meta"
    META_ANY: str = "Meta.<any>"
    PRECEDENCE: str = "Precedence"
    SOURCE_NS: str = "SourceNS"
    SOURCE_NAME: str = "SourceName"
    SOURCE_TYPE: str = "SourceType"

    def __str__(self):
        return str.__str__(self)
