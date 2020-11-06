import os
import time
import urllib.error
import urllib.request
from typing import List, Tuple, Optional

from touchstone.lib import exceptions
from touchstone.lib.managers.docker_manager import DockerManager
from touchstone.lib.networking.docker_network import DockerNetwork
from touchstone.lib.services.i_runnable import IRunnable
from touchstone.lib.services.i_service import IService
from touchstone.lib.services.i_testable import ITestable
from touchstone.lib.tests import Tests


class NetworkedService(IService, ITestable, IRunnable):
    def __init__(self, name: str, tests: Tests, dockerfile_path: Optional[str], docker_manager: DockerManager,
                 port: int, availability_endpoint: str, num_retries: int, seconds_between_retries: int,
                 log_directory: Optional[str], docker_network: DockerNetwork):
        self.__name = name
        self.__tests = tests
        self.__dockerfile_path = dockerfile_path
        self.__docker_manager = docker_manager
        self.__port = port
        self.__availability_endpoint = availability_endpoint
        self.__num_retries = num_retries
        self.__seconds_between_retries = seconds_between_retries
        self.__log_directory = log_directory
        self.__docker_network = docker_network

    def get_name(self):
        return self.__name

    def run_test(self, file_name, test_name) -> bool:
        return self.__tests.run(file_name, test_name, self.url())

    def run_all_tests(self) -> bool:
        self.__log('Running all tests...')
        did_pass = self.__tests.run_all(self.url())
        self.__log('Finished running all tests.\n')
        return did_pass

    def start(self, environment_vars: List[Tuple[str, str]] = []):
        if self.__dockerfile_path is not None:
            self.__log('Building and running Dockerfile...')
            tag = self.__docker_manager.build_dockerfile(self.__dockerfile_path)
            run_result = self.__docker_manager.run_background_image(tag, self.__port, environment_vars=environment_vars)
            self.__docker_network.set_container_id(run_result.container_id)
            self.__docker_network.set_port(run_result.port)
        else:
            self.__log('Service could not be started. A Dockerfile was not supplied. Check your "touchstone.yml".')

    def stop(self):
        if self.__docker_network.container_id():
            log_path = None
            if self.__log_directory:
                log_path = os.path.join(self.__log_directory, f'{self.__name}.log')
            self.__docker_manager.stop_container(self.__docker_network.container_id(), log_path)
            self.__docker_network.set_container_id(None)

    def wait_for_availability(self):
        full_endpoint = self.url() + self.__availability_endpoint
        self.__log(f'Attempting to connect to availability endpoint {full_endpoint}')
        for retry_num in range(self.__num_retries):
            try:
                code = urllib.request.urlopen(full_endpoint).getcode()
                if code % 200 < 100:
                    self.__log('Available\n')
                else:
                    self.__log(f'Availability endpoint returned non-2xx: "{code}"\n')
                return
            except (urllib.error.URLError, ConnectionResetError):
                self.__log(f'Not available. Retry {retry_num + 1} of {self.__num_retries}')
                time.sleep(self.__seconds_between_retries)
        raise exceptions.ServiceException('Could not connect to service\'s availability endpoint.')

    def is_running(self) -> bool:
        return self.__docker_network.container_id() is not None

    def url(self):
        port = self.__docker_network.port() if self.is_running() else self.__port
        return f'http://{self.__docker_network.external_host()}:{port}'

    def __log(self, message: str):
        print(f'{self.get_name()} :: {message}')
