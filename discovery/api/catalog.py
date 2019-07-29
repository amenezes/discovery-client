import attr

from discovery.api.base import BaseApi


@attr.s(slots=True)
class Catalog(BaseApi):
    endpoint = attr.ib(default='/catalog')

    def register(self, data, **kwargs):
        return self.client.put(
            f"{self.url}/register",
            data=data,
            params=kwargs
        )

    def deregister(self, data, **kwargs):
        return self.client.put(
            f"{self.url}/deregister",
            params=kwargs,
            data=data
        )

    def datacenters(self, **kwargs):
        return self.client.get(f"{self.url}/datacenters", params=kwargs)

    def nodes(self, **kwargs):
        return self.client.get(f"{self.url}/nodes", params=kwargs)

    def services(self, **kwargs):
        return self.client.get(f"{self.url}/services", params=kwargs)

    def service(self, name, **kwargs):
        return self.client.get(f"{self.url}/service/{name}", params=kwargs)

    def connect(self, service, **kwargs):
        return self.client.get(
            f"{self.url}/connect/{service}",
            params=kwargs
        )

    def node(self, node, **kwargs):
        return self.client.get(f"{self.url}/node/{node}", params=kwargs)
