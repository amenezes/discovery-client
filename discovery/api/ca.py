import attr

from discovery.api.base import BaseApi


@attr.s(frozen=True, slots=True)
class CA(BaseApi):
    endpoint = attr.ib(default='/connect/ca')

    def list(self, **kwargs):
        return self.client.get(f"{self.url}/roots", params=kwargs)

    def configuration(self, **kwargs):
        return self.client.get(
            f"{self.url}/configuration",
            params=kwargs
        )

    def update(self, data, **kwargs):
        return self.client.put(
            f"{self.url}/configuration",
            data=data,
            params=kwargs
        )
