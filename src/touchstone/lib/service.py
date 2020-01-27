import http
import http.client
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional, List, Tuple

from touchstone import common
from touchstone.lib import exceptions
from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.run_context import RunContext
from touchstone.lib.tests import Tests


class Service(object):
    def __init__(self, root: str, name: str, tests: Tests, dockerfile: str, host: str, port: int,
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
        self.__container_id: Optional[str] = None

    def start(self, run_contexts: List[RunContext]):
        if self.__dockerfile is not None:
            self.__log('Building and running Dockerfile...')
            dockerfile_path = os.path.abspath(os.path.join(self.__root, self.__dockerfile))
            tag = self.__docker_manager.build_dockerfile(dockerfile_path)
            environment_vars = self.__environment_vars_from_run_contexts(run_contexts)
            run_result = self.__docker_manager.run_image(tag, (self.__port, self.__port),
                                                         environment_vars=environment_vars)
            self.__container_id = run_result.container_id
            self.__port = run_result.port

    def stop(self):
        if self.__container_id:
            self.__docker_manager.stop_container(self.__container_id)
            self.__container_id = None

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

    def run_test(self, file_name, test_name) -> bool:
        self.__tests.service_url = self.url()
        return self.__tests.run(file_name, test_name)

    def run_all_tests(self) -> bool:
        self.__tests.service_url = self.url()
        return self.__tests.run_all()

    def is_running(self) -> bool:
        return self.__container_id is not None

    def __log(self, message: str):
        print(f'{self.name} :: {message}')

    def __environment_vars_from_run_contexts(self, run_contexts: List[RunContext]) -> List[Tuple[str, str]]:
        envs = []
        for run_context in run_contexts:
            name = run_context.name.upper()
            envs.append((f'TS_{name}_HOST', common.replace_host_with_docker_equivalent(run_context.network.host)))
            envs.append((f'TS_{name}_PORT', run_context.network.port))
            envs.append((f'TS_{name}_URL', run_context.network.url()))
        return envs
