import logging

from discovery import check, utils
from discovery.__version__ import __version__
from discovery.utils import service

log = logging.getLogger("discovery-client")
log.addHandler(logging.NullHandler())

__all__ = ["check", "service"]
