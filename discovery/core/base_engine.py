from abc import abstractmethod

import attr


@attr.s
class Engine:

    @abstractmethod
    def get(self, url, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def put(self, url, data=None, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete(self, url, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def post(self, url, data=None, **kwargs):
        raise NotImplementedError
