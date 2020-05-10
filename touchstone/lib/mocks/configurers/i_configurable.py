import abc


class IConfigurable(object):
    @abc.abstractmethod
    def get_config(self) -> dict:
        pass

    @abc.abstractmethod
    def merge_config(self, other: dict):
        pass
