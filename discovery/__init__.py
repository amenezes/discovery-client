import logging

from discovery.__version__ import __version__

log = logging.getLogger("discovery-client")
log.addHandler(logging.NullHandler())
