from touchstone import common
from touchstone.lib import exceptions


class ServiceConfig(object):
    def __init__(self):
        self.config: dict = {
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
        }

    def merge(self, other: dict):
        self.config = common.dict_merge(self.config, other)

    def verify(self):
        if self.config['type'] != 'networked' and self.config['type'] != 'executable':
            raise exceptions.TouchstoneException(
                f'Unknown service type: "{self.config["type"]}". Check your "touchstone.yml".')
        if self.config['dockerfile'] and self.config['docker_image']:
            raise exceptions.TouchstoneException(
                '"dockerfile" and "docker_image" cannot both be set. Check your "touchstone.yml".')
