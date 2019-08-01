import attr

from discovery.api.base import BaseApi


@attr.s(frozen=True, slots=True)
class Policy(BaseApi):
    endpoint = attr.ib(default='/acl/policy')

    def create(self, data, **kwargs):
        return self.client.put(f"{self.url}", params=kwargs, data=data)

    def read(self, policy_id, **kwargs):
        return self.client.get(f"{self.url}/{policy_id}", params=kwargs)

    def update(self, policy_id, data, **kwargs):
        return self.client.put(
            f"{self.url}/{policy_id}",
            params=kwargs,
            data=data
        )

    def delete(self, policy_id, **kwargs):
        return self.client.delete(f"{self.url}/{policy_id}", params=kwargs)

    def list(self, **kwargs):
        url = self.url.replace('policy', 'policies')
        return self.client.get(f"{url}", params=kwargs)
