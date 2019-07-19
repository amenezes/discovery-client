import attr

from discovery.core.aio_engine import AioEngine
from discovery.core.standard_engine import StandardEngine


@attr.s(str=False)
class Api:
    client = attr.ib()
    version = attr.ib(default='v1', init=False, repr=False)
    endpoint = attr.ib(default='/', init=False, repr=False)


def validate_engine(obj):
    if isinstance(obj, )