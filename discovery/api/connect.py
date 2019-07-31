import logging

import attr

from discovery.api.base import BaseApi
from discovery.api.ca import CA
from discovery.api.intention import Intentions

logging.getLogger(__name__).addHandler(logging.NullHandler())


@attr.s(slots=True)
class Connect(BaseApi):
    endpoint = attr.ib(default='/agent/connect')
    ca = attr.ib(
        type=CA,
        default=None
    )
    intentions = attr.ib(
        type=Intentions,
        default=None
    )

    def __attrs_post_init__(self):
        self.ca = CA(self.client)
        self.intentions = Intentions(self.client)

    def authorize(self, data, **kwargs):
        return self.client.post(
            f"{self.url}/authorize",
            params=kwargs,
            data=data
        )

    def ca_roots(self, **kwargs):
        return self.client.get(f"{self.url}/ca/roots", params=kwargs)

    def ca_leaf(self, service, **kwargs):
        return self.client.get(
            f"{self.url}/ca/leaf/{service}", params=kwargs
        )

    def proxy(self, proxy_id, **kwargs):
        logging.warning('Deprecated. https://www.consul.io/docs/connect/proxies/managed-deprecated.html')
        return self.client.get(
            f"{self.url}/proxy/{proxy_id}", params=kwargs
        )
