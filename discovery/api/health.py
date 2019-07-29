import attr

from discovery.api.base import BaseApi


@attr.s(frozen=True, slots=True)
class Health(BaseApi):
    endpoint = attr.ib(default='/health')

    def node(self, node):
        return self.client.get(f"{self.url}/node/{node}")

    def checks(self, service):
        return self.client.get(f"{self.url}/checks/{service}")

    def service(self, service):
        return self.client.get(f"{self.url}/service/{service}")

    def connect(self, service):
        return self.client.get(f"{self.url}/connect/{service}")

    def state(self, state):
        if not isinstance(state, str):
            raise TypeError('state must be a str.')
        elif state.lower() not in ['passing', 'warning', 'critical']:
            raise ValueError(
                'Valid values are "passing", "warning", and "critical"'
            )
        return self.client.get(f"{self.url}/state/{state}")
