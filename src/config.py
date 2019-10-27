class Config(object):
    def __init__(self,
                 service_host='localhost',
                 service_port=8080,
                 service_dockerfile=None,
                 service_base_url='',
                 service_availability_endpoint='',
                 num_retries=20,
                 seconds_between_retries=10):
        self.service_host = service_host
        self.service_port = service_port
        self.service_dockerfile = service_dockerfile
        self.service_base_url = service_base_url
        self.service_availability_endpoint = service_availability_endpoint
        self.num_retries = num_retries
        self.seconds_between_retries = seconds_between_retries
        self.host_port = None

    def service_url(self):
        port = self.service_port
        if self.host_port is not None:
            port = self.host_port
        return f'http://{self.service_host}:{port}{self.service_base_url}'

    def set_host_port(self, host_port):
        self.host_port = host_port
