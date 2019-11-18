from touchstone_config import TouchstoneConfig


class Config(object):
    def __init__(self,
                 service_host: str = TouchstoneConfig.instance().config['host'],
                 service_port: int = 8080,
                 service_exposed_port: int = None,
                 service_dockerfile: str = None,
                 service_base_url: str = '',
                 service_availability_endpoint: str = '',
                 num_retries: int = 20,
                 seconds_between_retries: int = 10):
        self.service_host: str = service_host
        self.service_port: int = service_port
        if service_exposed_port is None:
            service_exposed_port = service_port
        self.service_exposed_port: int = service_exposed_port
        self.service_dockerfile: str = service_dockerfile
        self.service_base_url: str = service_base_url
        self.service_availability_endpoint: str = service_availability_endpoint
        self.num_retries: int = num_retries
        self.seconds_between_retries: int = seconds_between_retries

        self.service_url: str = f'http://{self.service_host}:{self.service_exposed_port}{self.service_base_url}'
