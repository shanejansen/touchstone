from touchstone.lib import exceptions
from touchstone.lib.configurers.BasicConfigurer import BasicConfigurer
from touchstone.lib.configurers.i_configurable import IConfigurable


class TouchstoneConfig(IConfigurable):
    def __init__(self, root):
        self.__basic_configurer = BasicConfigurer({
            'root': root,
            'services': [],
            'dependencies': []
        })

    def get_config(self) -> dict:
        return self.__basic_configurer.get_config()

    def merge_config(self, other: dict):
        self.__basic_configurer.merge_config(other)

    def verify(self):
        if self.__basic_configurer.get_config()['services'] is None:
            raise exceptions.TouchstoneException(f'"services" has not been set. Check your "touchstone.yml".')
        if self.__basic_configurer.get_config()['dependencies'] is None:
            raise exceptions.TouchstoneException(f'"dependencies" has not been set. Check your "touchstone.yml".')
