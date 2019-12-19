import http
import http.client
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

import time

from touchstone.lib.configs.service_config import ServiceConfig
from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.tests import Tests


class Service(object):
    def __init__(self, service_config: ServiceConfig, tests: Tests):
        self.service_config = service_config
        self.tests = tests
        self.container_name: Optional[str] = None

    def name(self):
        return self.service_config.config['name']

    def start(self):
        if self.service_config.config['dockerfile'] is not None:
            self.__log('Building and running Dockerfile...')
            dockerfile_path = os.path.abspath(
                os.path.join(TouchstoneConfig.instance().config["root"], self.service_config.config['dockerfile']))
            tag = DockerManager.instance().build_dockerfile(dockerfile_path)
            service_port = self.service_config.config['port']
            self.container_name = DockerManager.instance().run_image(tag, [(service_port, service_port)])

    def stop(self):
        if self.container_name:
            DockerManager.instance().stop_container(self.container_name)
            self.container_name = None

    def run_tests(self) -> bool:
        if self.__wait_for_availability() is False:
            self.__log('Could not connect to service\'s availability endpoint.\n')
            return False

        self.__log('Available. Running tests\n')
        return self.tests.run()

    def __wait_for_availability(self) -> bool:
        full_endpoint = self.service_config.config['url'] + self.service_config.config['availability_endpoint']
        self.__log(f'Attempting to connect to availability endpoint {full_endpoint}')
        try:
            for retry_num in range(self.service_config.config['num_retries']):
                try:
                    urllib.request.urlopen(full_endpoint).read()
                    return True
                except (urllib.error.URLError, http.client.RemoteDisconnected):
                    self.__log(f'Not available. Retry {retry_num + 1} of {self.service_config.config["num_retries"]}')
                    time.sleep(self.service_config.config['seconds_between_retries'])
        except KeyboardInterrupt:
            return False
        return False

    def __log(self, message: str):
        print(f'{self.service_config.config["name"]} :: {message}')
