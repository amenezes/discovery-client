"""Enum to better filter consul options."""

from enum import Enum


class Filter(Enum):
    """A enum to better filter options on consul clients."""

    FIRST_ITEM = 0
    PAYLOAD = 1
    DEFAULT_TIMEOUT = 30
