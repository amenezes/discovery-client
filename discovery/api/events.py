import attr

from discovery.api.base import BaseApi


@attr.s(slots=True)
class Events(BaseApi):
    endpoint = attr.ib(default='/event')

    def fire(self, name, data, **kwargs):
        return self.client.put(
            f"{self.url}/fire/{name}",
            params=kwargs,
            data=data
        )

    def list(self, key, **kwargs):
        return self.client.get(
            f"{self.url}/list",
            params=kwargs
        )
