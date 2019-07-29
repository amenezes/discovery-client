import attr

from discovery.api.base import BaseApi


@attr.s(slots=True)
class Keyring(BaseApi):
    endpoint = attr.ib(default='/operator/keyring')

    def list(self):
        return self.client.get(f"{self.url}")

    def add(self, data):
        return self.client.post(f"{self.url}", data=data)

    def change(self, data):
        return self.client.put(f"{self.url}", data=data)

    def delete(self, data):
        return self.client.delete(f"{self.url}", data=data)
