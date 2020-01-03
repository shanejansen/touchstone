from touchstone.lib import common
from touchstone.lib.configs.touchstone_config import TouchstoneConfig


class ServiceConfig(object):
    def __init__(self):
        self.config: dict = {
            'name': 'Unnamed Service',
            'host': TouchstoneConfig.instance().config['host'],
            'port': 8080,
            'dockerfile': None,
            'availability_endpoint': '',
            'num_retries': 20,
            'seconds_between_retries': 5
        }
        self.__build_url()

    def merge(self, other: dict):
        self.config = common.dict_merge(self.config, other)
        self.__build_url()

    def __build_url(self):
        self.config['url'] = f'http://{self.config["host"]}:{self.config["port"]}'
