import os
from typing import List, Tuple, Optional

from touchstone.lib import exceptions
from touchstone.lib.health_checks.blocking_health_check import BlockingHealthCheck
from touchstone.lib.health_checks.docker_health_check import DockerHealthCheck
from touchstone.lib.health_checks.http_health_check import HttpHealthCheck
from touchstone.lib.managers.docker_manager import DockerManager
from touchstone.lib.networking.docker_network import DockerNetwork
from touchstone.lib.networking.i_network import INetwork
from touchstone.lib.nodes.i_networkable import INetworkable
from touchstone.lib.nodes.services.i_runnable import IRunnable
from touchstone.lib.nodes.services.i_service import IService
from touchstone.lib.nodes.services.i_testable import ITestable
from touchstone.lib.tests import Tests


class DockerRunnableService(IService, ITestable, IRunnable, INetworkable):
    def __init__(self, name: str, tests: Optional[Tests], dockerfile_path: Optional[str], docker_image: Optional[str],
                 docker_options: Optional[str], docker_manager: DockerManager, port: int, availability_endpoint: str,
                 log_directory: Optional[str], docker_network: DockerNetwork,
                 blocking_health_check: BlockingHealthCheck):
        self.__name = name
        self.__tests = tests
        self.__dockerfile_path = dockerfile_path
        self.__docker_image = docker_image
        self.__docker_options = docker_options
        self.__docker_manager = docker_manager
        self.__port = port
        self.__availability_endpoint = availability_endpoint
        self.__log_directory = log_directory
        self.__docker_network = docker_network
        self.__blocking_health_check = blocking_health_check

    def get_name(self):
        return self.__name

    def run_test(self, file_name, test_name) -> bool:
        if not self.__tests:
            return True
        return self.__tests.run(file_name, test_name, self.url())

    def run_all_tests(self) -> bool:
        if not self.__tests:
            return True
        self.__log('Running all tests...')
        did_pass = self.__tests.run_all(self.url())
        self.__log('Finished running all tests.\n')
        return did_pass

    def start(self, environment_vars: List[Tuple[str, str]] = []):
        if self.__dockerfile_path is None and self.__docker_image is None:
            raise exceptions.ServiceException(
                f'{self.get_name()} could not be started. A Dockerfile or Docker image was not supplied. Check your '
                f'"touchstone.yml".')
        docker_artifact = None
        if self.__dockerfile_path is not None:
            self.__log('Building and running Dockerfile...')
            docker_artifact = self.__docker_manager.build_dockerfile(self.__dockerfile_path)
        elif self.__docker_image is not None:
            self.__log('Running Docker image...')
            docker_artifact = self.__docker_image
        log_path = None
        if self.__log_directory:
            log_path = os.path.join(self.__log_directory, f'{self.__name}.log')
        run_result = self.__docker_manager.run_background_image(docker_artifact, self.__port,
                                                                environment_vars=environment_vars,
                                                                hostname=self.__name,
                                                                log_path=log_path,
                                                                options=self.__docker_options)
        self.__docker_network.set_container_id(run_result.container_id)
        self.__docker_network.set_external_port(run_result.external_port)

    def stop(self):
        if self.__docker_network.container_id():
            self.__docker_manager.stop_container(self.__docker_network.container_id())
            self.__docker_network.set_container_id(None)

    def is_running(self) -> bool:
        return self.__docker_network.container_id() is not None

    def wait_until_healthy(self):
        target = self.__blocking_health_check.get_target()
        if isinstance(target, HttpHealthCheck):
            target.set_url(self.url() + self.__availability_endpoint)
        elif isinstance(target, DockerHealthCheck):
            target.set_container_id(self.__docker_network.container_id())
        else:
            raise exceptions.ServiceException('Health check type not supported.')
        is_healthy = self.__blocking_health_check.wait_until_healthy()
        if not is_healthy:
            raise exceptions.ServiceException('Could not connect to service\'s availability endpoint.')

    def url(self):
        port = self.__docker_network.external_port() if self.is_running() else self.__port
        return f'http://{self.__docker_network.external_host()}:{port}'

    def get_network(self) -> INetwork:
        return self.__docker_network

    def __log(self, message: str):
        print(f'{self.get_name()} :: {message}')
