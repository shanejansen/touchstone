import os
from typing import List, Tuple, Optional

from touchstone.lib import exceptions
from touchstone.lib.health_checks.blocking_health_check import BlockingHealthCheck
from touchstone.lib.health_checks.docker_health_check import DockerHealthCheck
from touchstone.lib.health_checks.http_health_check import HttpHealthCheck
from touchstone.lib.health_checks.i_health_checkable import IHealthCheckable
from touchstone.lib.managers.docker_manager import DockerManager
from touchstone.lib.networking.docker_network import DockerNetwork
from touchstone.lib.services.i_runnable import IRunnable
from touchstone.lib.services.i_service import IService
from touchstone.lib.services.i_testable import ITestable
from touchstone.lib.tests import Tests


class NetworkedService(IService, ITestable, IRunnable):
    def __init__(self, name: str, tests: Tests, dockerfile_path: Optional[str], docker_options: Optional[str],
                 docker_manager: DockerManager, port: int, availability_endpoint: str, log_directory: Optional[str],
                 docker_network: DockerNetwork, health_check: IHealthCheckable,
                 blocking_health_check: BlockingHealthCheck):
        self.__name = name
        self.__tests = tests
        self.__dockerfile_path = dockerfile_path
        self.__docker_options = docker_options
        self.__docker_manager = docker_manager
        self.__port = port
        self.__availability_endpoint = availability_endpoint
        self.__log_directory = log_directory
        self.__docker_network = docker_network
        self.__health_check = health_check
        self.__blocking_health_check = blocking_health_check

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
            run_result = self.__docker_manager.run_background_image(tag, self.__port, environment_vars=environment_vars,
                                                                    options=self.__docker_options)
            self.__docker_network.set_container_id(run_result.container_id)
            self.__docker_network.set_external_port(run_result.external_port)
        else:
            self.__log('Service could not be started. A Dockerfile was not supplied. Check your "touchstone.yml".')

    def stop(self):
        if self.__docker_network.container_id():
            log_path = None
            if self.__log_directory:
                log_path = os.path.join(self.__log_directory, f'{self.__name}.log')
            self.__docker_manager.stop_container(self.__docker_network.container_id(), log_path)
            self.__docker_network.set_container_id(None)

    def is_running(self) -> bool:
        return self.__docker_network.container_id() is not None

    def wait_until_healthy(self):
        if isinstance(self.__health_check, HttpHealthCheck):
            self.__health_check.set_url(self.url() + self.__availability_endpoint)
        if isinstance(self.__health_check, DockerHealthCheck):
            self.__health_check.set_container_id(self.__docker_network.container_id())
        is_healthy = self.__blocking_health_check.wait_until_healthy()
        if not is_healthy:
            raise exceptions.ServiceException('Could not connect to service\'s availability endpoint.')

    def url(self):
        port = self.__docker_network.external_port() if self.is_running() else self.__port
        return f'http://{self.__docker_network.external_host()}:{port}'

    def __log(self, message: str):
        print(f'{self.get_name()} :: {message}')
