import yaml

from touchstone import common
from touchstone.lib.mocks.configurers.i_configurable import IConfigurable


class FileConfigurer(IConfigurable):
    def __init__(self, config_path: str = None):
        self.__config_path = config_path
        self.__override_config = {}

    def get_config(self) -> dict:
        if not self.__config_path:
            return {}
        with open(self.__config_path, 'r') as file:
            config = yaml.safe_load(file)
        return common.dict_merge(config, self.__override_config)

    def merge_config(self, other: dict):
        self.__override_config = other
