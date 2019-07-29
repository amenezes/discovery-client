import attr

from discovery.api.base import BaseApi


@attr.s(slots=True)
class License(BaseApi):
    endpoint = attr.ib(default='/operator/license')

    def current(self, **kwargs):
        return self.client.get(f"{self.url}", params=kwargs)

    def update(self, data, **kwargs):
        return self.client.put(f"{self.url}", params=kwargs, data=data)

    def reset(self, **kwargs):
        return self.client.delete(f"{self.url}", params=kwargs)
