import attr

from discovery.api.base import BaseApi


@attr.s(slots=True)
class Config(BaseApi):
    endpoint = attr.ib(default='/config')

    def config_entry_kind_is_valid(self, kind):
        if not isinstance(kind, str):
            raise TypeError('kind must be a str.')
        elif kind.lower() not in ['service-defaults', 'proxy-defaults']:
            raise ValueError(
                'Valid values are "service-defaults" and "proxy-defaults".'
            )
        return True

    def apply(self, data, **kwargs):
        return self.client.put(f"{self.url}", params=kwargs, data=data)

    def get(self, kind, name, **kwargs):
        if self.config_entry_kind_is_valid(kind):
            return self.client.get(f"{self.url}/{kind}/{name}", params=kwargs)

    def list(self, kind, **kwargs):
        if self.config_entry_kind_is_valid(kind):
            return self.client.get(f"{self.url}/{kind}", params=kwargs)

    def delete(self, kind, name, **kwargs):
        if self.config_entry_kind_is_valid(kind):
            return self.client.delete(f"{self.url}/{kind}/{name}", params=kwargs)
