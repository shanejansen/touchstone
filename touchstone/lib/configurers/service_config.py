from touchstone.lib import exceptions
from touchstone.lib.configurers.BasicConfigurer import BasicConfigurer
from touchstone.lib.configurers.i_configurable import IConfigurable


class ServiceConfig(IConfigurable):
    def __init__(self):
        self.__basic_configurer = BasicConfigurer({
            'type': 'networked',
            'name': 'unnamed-service',
            'tests': './tests',
            'port': 8080,
            'dockerfile': None,
            'docker_image': None,
            'docker_options': None,
            'availability_endpoint': None,
            'num_retries': 20,
            'seconds_between_retries': 5,
            'develop_command': ''
        })

    def get_config(self) -> dict:
        return self.__basic_configurer.get_config()

    def merge_config(self, other: dict):
        self.__basic_configurer.merge_config(other)

    def verify(self):
        service_type = self.__basic_configurer.get_config()['type']
        if service_type != 'networked' and service_type != 'executable':
            raise exceptions.TouchstoneException(
                f'Unknown service type: "{service_type}". Check your "touchstone.yml".')
        if self.__basic_configurer.get_config()['dockerfile'] and self.__basic_configurer.get_config()['docker_image']:
            raise exceptions.TouchstoneException(
                '"dockerfile" and "docker_image" cannot both be set. Check your "touchstone.yml".')
