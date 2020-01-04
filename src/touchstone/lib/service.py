import http
import http.client
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

from touchstone.lib import exceptions
from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.tests import Tests


class Service(object):
    def __init__(self, root: str, name: str, tests: Tests, dockerfile: str, host: str, port: str,
                 availability_endpoint: str, num_retries: int, seconds_between_retries: int,
                 docker_manager: DockerManager):
        self.name = name
        self.__root = root
        self.__tests = tests
        self.__dockerfile = dockerfile
        self.__host = host
        self.__port = port
        self.__availability_endpoint = availability_endpoint
        self.__num_retries = num_retries
        self.__seconds_between_retries = seconds_between_retries
        self.__docker_manager = docker_manager
        self.__container_name: Optional[str] = None

    def start(self):
        if self.__dockerfile is not None:
            self.__log('Building and running Dockerfile...')
            dockerfile_path = os.path.abspath(os.path.join(self.__root, self.__dockerfile))
            tag = self.__docker_manager.build_dockerfile(dockerfile_path)
            self.__container_name = self.__docker_manager.run_image(tag, [(self.__port, self.__port)])

    def stop(self):
        if self.__container_name:
            self.__docker_manager.stop_container(self.__container_name)
            self.__container_name = None

    def url(self):
        return f'http://{self.__host}:{self.__port}'

    def wait_for_availability(self):
        full_endpoint = self.url() + self.__availability_endpoint
        self.__log(f'Attempting to connect to availability endpoint {full_endpoint}')
        for retry_num in range(self.__num_retries):
            try:
                urllib.request.urlopen(full_endpoint).read()
                self.__log('Available\n')
                return
            except (urllib.error.URLError, http.client.RemoteDisconnected):
                self.__log(f'Not available. Retry {retry_num + 1} of {self.__num_retries}')
                time.sleep(self.__seconds_between_retries)
        raise exceptions.ServiceException('Could not connect to service\'s availability endpoint.')

    def run_tests(self) -> bool:
        self.__tests.service_url = self.url()
        return self.__tests.run()

    def is_running(self) -> bool:
        return self.__container_name is not None

    def __log(self, message: str):
        print(f'{self.name} :: {message}')
