from configs.touchstone_config import TouchstoneConfig


class ServiceConfig(object):
    def __init__(self):
        self.config: dict = {
            'name': 'Unnamed Service',
            'host': TouchstoneConfig.instance().config['host'],
            'port': 8080,
            'dockerfile': None,
            'base_url': '',
            'availability_endpoint': '',
            'num_retries': 20,
            'seconds_between_retries': 10
        }

        self.config['url'] = f'http://{self.config["host"]}' \
                             f':{self.config["port"]}' \
                             f'{self.config["base_url"]}'

    def merge(self, other: dict):
        self.config = dict(list(self.config.items()) + list(other.items()))
