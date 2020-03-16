"""Enum to better filter consul options."""

from enum import Enum, unique


@unique
class Filter(Enum):
    """A enum to better filter options on consul clients."""

    FIRST_ITEM = 0
    PAYLOAD = 1
