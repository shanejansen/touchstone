from touchstone_config import TouchstoneConfig


class Config(object):
    def __init__(self,
                 service_host=TouchstoneConfig.instance().config['host'],
                 service_port=8080,
                 service_exposed_port=None,
                 service_dockerfile=None,
                 service_base_url='',
                 service_availability_endpoint='',
                 num_retries=20,
                 seconds_between_retries=10):
        self.service_host = service_host
        self.service_port = service_port
        if service_exposed_port is None:
            service_exposed_port = service_port
        self.service_exposed_port = service_exposed_port
        self.service_dockerfile = service_dockerfile
        self.service_base_url = service_base_url
        self.service_availability_endpoint = service_availability_endpoint
        self.num_retries = num_retries
        self.seconds_between_retries = seconds_between_retries

        self.service_url = f'http://{self.service_host}:{self.service_exposed_port}{self.service_base_url}'
