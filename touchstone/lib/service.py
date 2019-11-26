import http
import http.client
import os
import time
import urllib.error
import urllib.parse
import urllib.request

from touchstone.lib.configs.service_config import ServiceConfig
from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.tests import Tests


class Service(object):
    def __init__(self, service_config: ServiceConfig, tests: Tests):
        self.service_config = service_config
        self.tests = tests

    def run_tests(self) -> bool:
        if TouchstoneConfig.instance().config['dev'] is False and self.service_config.config['dockerfile'] is not None:
            self.__log('Building and running Dockerfile...')
            dockerfile_path = os.path.abspath(
                os.path.join(TouchstoneConfig.instance().config["root"], self.service_config.config['dockerfile']))
            tag = DockerManager.instance().build_dockerfile(dockerfile_path)
            DockerManager.instance().run_image(tag, self.service_config.config['port'],
                                               self.service_config.config['port'])

        if self.__wait_for_availability() is False:
            self.__log('Could not connect to service\'s availability endpoint.\n')
            return False

        self.__log('Available. Running tests\n')
        return self.tests.run()

    def __wait_for_availability(self) -> bool:
        response = None
        full_endpoint = self.service_config.config['url'] + self.service_config.config['availability_endpoint']
        self.__log(f'Attempting to connect to availability endpoint {full_endpoint}')
        for retry_num in range(self.service_config.config['num_retries']):
            try:
                response = urllib.request.urlopen(full_endpoint).read()
                return True
            except (urllib.error.URLError, http.client.RemoteDisconnected):
                self.__log(f'Not available. Retry {retry_num + 1} of {self.service_config.config["num_retries"]}')
                time.sleep(self.service_config.config['seconds_between_retries'])
        if response is None:
            return False
        return True

    def __log(self, message: str):
        print(f'{self.service_config.config["name"]} :: {message}')
