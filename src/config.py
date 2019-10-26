import sys


class Config(object):
    def __init__(self,
                 service_port,
                 service_dockerfile=None,
                 service_host=None,
                 service_base_url='',
                 service_availability_endpoint='',
                 num_retries=20,
                 seconds_between_retries=10):
        if service_dockerfile is None and service_host is None:
            print('Either "service_dockerfile" or "service_host" must be specified in your Config.')
            sys.exit(1)
        if service_dockerfile is not None:
            service_host = 'service'
        self.service_host = service_host
        self.service_url = f'http://{service_host}:{service_port}{service_base_url}'
        self.service_availability_endpoint = service_availability_endpoint
        self.num_retries = num_retries
        self.seconds_between_retries = seconds_between_retries
