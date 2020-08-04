from touchstone import common
from touchstone.lib import exceptions


class ServiceConfig(object):
    def __init__(self, host):
        self.config: dict = {
            'type': 'networked',
            'name': 'unnamed-service',
            'tests': './tests',
            'host': host,
            'port': 8080,
            'dockerfile': None,
            'availability_endpoint': '',
            'num_retries': 20,
            'seconds_between_retries': 5,
            'develop_command': ''
        }
        service_type = self.config['type']
        if service_type != 'networked' and service_type != 'executable':
            raise exceptions.TouchstoneException(
                f'Unknown service type: "{service_type}". Check your "touchstone.yml".')

    def merge(self, other: dict):
        self.config = common.dict_merge(self.config, other)
