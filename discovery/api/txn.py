import attr

from discovery.api.base import BaseApi


@attr.s(frozen=True, slots=True)
class Txn(BaseApi):
    endpoint = attr.ib(default='/txn')

    def create(self, data, **kwargs):
        return self.client.put(
            f'{self.url}',
            data=data,
            params=kwargs
        )
