from touchstone import common


class ServiceConfig(object):
    def __init__(self, host):
        self.config: dict = {
            'name': 'unnamed-service',
            'tests': './tests',
            'host': host,
            'port': 8080,
            'dockerfile': None,
            'availability_endpoint': '',
            'num_retries': 20,
            'seconds_between_retries': 5
        }

    def merge(self, other: dict):
        self.config = common.dict_merge(self.config, other)
