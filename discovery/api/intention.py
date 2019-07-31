import attr

from discovery.api.base import BaseApi


@attr.s(slots=True)
class Intentions(BaseApi):
    endpoint = attr.ib(default='/connect/intentions')

    def by_is_valid(self, by):
        if by.lower() not in ['source', 'destination']:
            raise ValueError('by must be: "source" or "destination"')
        return True

    def create(self, data, **kwargs):
        return self.client.post(f"{self.url}", params=kwargs, data=data)

    def read(self, uuid, **kwargs):
        return self.client.get(f"{self.url}/{uuid}", params=kwargs)

    def list(self, **kwargs):
        return self.client.get(f"{self.url}", params=kwargs)

    def update(self, uuid, data, **kwargs):
        return self.client.put(
            f"{self.url}/{uuid}",
            params=kwargs,
            data=data
        )

    def delete(self, uuid, **kwargs):
        return self.client.delete(
            f"{self.url}/{uuid}",
            params=kwargs
        )

    def check(self, source, destination, **kwargs):
        return self.client.get(
            f"{self.url}/check?source={source}&destination={destination}",
            params=kwargs
        )

    def match(self, by, name, **kwargs):
        if self.by_is_valid(by):
            return self.client.get(
                f"{self.url}/match?by={by}&name={name}",
                params=kwargs
            )
