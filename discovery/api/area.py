import attr

from discovery.api.base import BaseApi


@attr.s(frozen=True, slots=True)
class Area(BaseApi):
    endpoint = attr.ib(default='/operator/area')

    def create(self, data, **kwargs):
        return self.client.post(f"{self.url}", params=kwargs, data=data)

    def list(self, uuid=None, **kwargs):
        if uuid:
            uri = f"{self.url}/{uuid}"
        else:
            uri = f"{self.url}"
        return self.client.get(uri, params=kwargs)

    def update(self, uuid, data, **kwargs):
        return self.client.put(
            f"{self.url}/{uuid}",
            params=kwargs,
            data=data
        )

    def delete(self, uuid, **kwargs):
        return self.client.delete(f"{self.url}/{uuid}", params=kwargs)

    def join(self, uuid, data, **kwargs):
        return self.client.put(
            f"{self.url}/{uuid}/join",
            params=kwargs,
            data=data
        )

    def members(self, uuid, **kwargs):
        return self.client.get(f"{self.url}/{uuid}/members", params=kwargs)
