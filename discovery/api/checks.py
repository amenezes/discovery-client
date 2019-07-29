import json

import attr

from discovery.api.base import BaseApi


@attr.s(frozen=True, slots=True)
class Checks(BaseApi):
    endpoint = attr.ib(default='/agent/check')

    def checks(self):
        return self.client.get(f"{self.url}s")

    def register(self, data):
        return self.client.put(f"{self.url}/register", data=data)

    def deregister(self, check_id):
        return self.client.put(f"{self.url}/deregister/{check_id}")

    def check_pass(self, check_id, notes=''):
        return self.client.put(f"{self.url}/pass/{check_id}", data=notes)

    def check_warn(self, check_id, notes=''):
        return self.client.put(f"{self.url}/warn/{check_id}", data=notes)

    def check_fail(self, check_id, notes=''):
        return self.client.put(f"{self.url}/fail/{check_id}", data=notes)

    def check_update(self, check_id, status, output=''):
        if not isinstance(status, str):
            raise TypeError('status must be a str.')
        if status.lower() not in ['passing', 'warning', 'critical']:
            raise ValueError(
                'Valid values are "passing", "warning", and "critical"'
            )
        data = dict(status=status, output=output)
        return self.client.put(
            f"{self.url}/update/{check_id}",
            data=json.dumps(data)
        )
