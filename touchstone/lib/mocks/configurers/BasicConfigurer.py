from touchstone import common
from touchstone.lib.mocks.configurers.i_configurable import IConfigurable


class BasicConfigurer(IConfigurable):
    def __init__(self, default_config: dict):
        self.__config = default_config

    def get_config(self) -> dict:
        return self.__config

    def merge_config(self, other: dict):
        self.__config = common.dict_merge(self.__config, other)
