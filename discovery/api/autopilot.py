import attr

from discovery.api.base import BaseApi


@attr.s(slots=True)
class AutoPilot(BaseApi):
    endpoint = attr.ib(default='/operator/autopilot')

    def read_configuration(self, **kwargs):
        return self.client.get(f"{self.url}/configuration", params=kwargs)

    def update_configuration(self, data, **kwargs):
        return self.client.put(
            f"{self.url}/configuration",
            data=data,
            params=kwargs
        )

    def read_health(self, **kwargs):
        return self.client.get(f"{self.url}/health", params=kwargs)
