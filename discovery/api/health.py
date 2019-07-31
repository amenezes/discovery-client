import attr

from discovery.api.base import BaseApi


@attr.s(frozen=True, slots=True)
class Health(BaseApi):
    endpoint = attr.ib(default='/health')

    def node(self, node, **kwargs):
        return self.client.get(f"{self.url}/node/{node}", params=kwargs)

    def checks(self, service, **kwargs):
        return self.client.get(f"{self.url}/checks/{service}", params=kwargs)

    def service(self, service, **kwargs):
        return self.client.get(f"{self.url}/service/{service}", params=kwargs)

    def connect(self, service, **kwargs):
        return self.client.get(f"{self.url}/connect/{service}", params=kwargs)

    def state(self, state, **kwargs):
        if not isinstance(state, str):
            raise TypeError('state must be a str.')
        elif state.lower() not in ['passing', 'warning', 'critical']:
            raise ValueError(
                'Valid values are "passing", "warning", and "critical"'
            )
        return self.client.get(f"{self.url}/state/{state}", params=kwargs)
