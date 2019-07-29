import attr

from discovery.api.base import BaseApi


@attr.s(slots=True)
class Coordinate(BaseApi):
    endpoint = attr.ib(default='/coordinate')

    def read_wan(self, **kwargs):
        return self.client.get(f"{self.url}/datacenters", params=kwargs)

    def read_lan(self, **kwargs):
        return self.client.get(f"{self.url}/nodes", params=kwargs)

    def read_lan_node(self, node, **kwargs):
        return self.client.get(f"{self.url}/node/{node}", params=kwargs)

    def update_lan_node(self, data, **kwargs):
        return self.client.put(
            f"{self.url}/update", params=kwargs, data=data
        )
