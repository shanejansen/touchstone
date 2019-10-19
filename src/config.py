class Config(object):
    def __init__(self,
                 service_url='http://app:8080/api/v1/',
                 availability_endpoint='management/health',
                 num_retries=20,
                 seconds_between_retries=10):
        self.service_url = service_url
        self.availability_endpoint = availability_endpoint
        self.num_retries = num_retries
        self.seconds_between_retries = seconds_between_retries
