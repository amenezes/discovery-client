from abc import ABC

import attr

from discovery.core.engine.base import Engine


@attr.s(slots=True)
class BaseApi(ABC):
    client = attr.ib(
        type=Engine,
        validator=attr.validators.instance_of(Engine)
    )
    endpoint = attr.ib(type=str, default='/')
    version = attr.ib(type=str, default='v1')
    _url = attr.ib(
        type=str,
        default=None,
        converter=attr.converters.default_if_none(
            '{base}/{version}{endpoint}'
        )
    )

    @property
    def url(self):
        return self._url.format(
            base=self.client.url,
            version=self.version,
            endpoint=self.endpoint
        )
