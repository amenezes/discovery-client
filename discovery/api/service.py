from urllib.parse import quote_plus

import attr

from discovery.api.base import BaseApi


@attr.s(frozen=True, slots=True)
class Service(BaseApi):
    endpoint = attr.ib(default='/agent/service')
    local_service_health = {
        200: 'All healthchecks of every matching service instance are passing',
        400: 'Bad parameter (missing service name of id)',
        404: 'No such service id or name',
        429: 'Some healthchecks are passing, at least one is warning',
        503: 'At least one of the healthchecks is critical'
    }

    def services(self, **kwargs):
        return self.client.get(f"{self.url}s", params=kwargs)

    def service(self, service_id, **kwargs):
        return self.client.get(f"{self.url}/{service_id}", params=kwargs)

    def configuration(self, service_id, **kwargs):
        return self.client.get(f"{self.url}/{service_id}", params=kwargs)

    def register(self, data, **kwargs):
        print(data)
        return self.client.put(
            f"{self.url}/register",
            params=kwargs,
            data=data
        )

    def deregister(self, service_id, **kwargs):
        return self.client.put(
            f"{self.url}/deregister/{service_id}",
            params=kwargs
        )

    def maintenance(self, service_id, enable, reason='', **kwargs):
        reason = quote_plus(reason)
        enable = str(enable).lower()
        return self.client.put(
            f"{self.url}/maintenance/{service_id}?enable={enable}&reason={reason}",
            params=kwargs
        )

    def get_local_service_health(self, name, format='json', **kwargs):
        if self.format_is_valid(format):
            url = self.url.replace('service', 'health')
            return self.client.get(
                f"{url}/service/name/{name}",
                params=kwargs
            )

    def format_is_valid(self, format):
        if format not in ['json', 'text']:
            raise ValueError('format must be: "json" or "text".')
        return True

    def describe_health_code(self, code):
        if code not in self.local_service_health.keys():
            return (
                'Invalid code. Please see: '
                'https://www.consul.io/'
                'api/agent/service.html#get-local-service-health'
            )
        return self.local_service_health.get(code)

    def get_local_service_health_by_id(self, service_id, **kwargs):
        url = self.url.replace('service', 'health')
        return self.client.get(
            f"{url}/service/id/{service_id}",
            params=kwargs
        )
