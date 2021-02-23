import os
import subprocess
from typing import List, Tuple, Optional

from touchstone.lib import exceptions
from touchstone.lib.managers.docker_manager import DockerManager
from touchstone.lib.nodes.services.i_executable import IExecutable
from touchstone.lib.nodes.services.i_service import IService
from touchstone.lib.nodes.services.i_testable import ITestable
from touchstone.lib.tests import Tests


class DockerExecutableService(IService, ITestable, IExecutable):
    def __init__(self, name: str, is_dev_mode: bool, tests: Optional[Tests], dockerfile_path: Optional[str],
                 docker_image: Optional[str], docker_options: Optional[str], docker_manager: DockerManager,
                 develop_command: str, log_directory: Optional[str]):
        self.__name = name
        self.__is_dev_mode = is_dev_mode
        self.__tests = tests
        self.__dockerfile_path = dockerfile_path
        self.__docker_image = docker_image
        self.__docker_options = docker_options
        self.__docker_manager = docker_manager
        self.__develop_command = develop_command
        self.__log_directory = log_directory

    def get_name(self):
        return self.__name

    def run_test(self, file_name, test_name) -> bool:
        if not self.__tests:
            return True
        return self.__tests.run(file_name, test_name)

    def run_all_tests(self) -> bool:
        if not self.__tests:
            return True
        self.__log('Running all tests...')
        did_pass = self.__tests.run_all()
        self.__log('Finished running all tests.\n')
        return did_pass

    def execute(self, environment_vars: List[Tuple[str, str]] = []):
        if self.__is_dev_mode:
            subprocess.run(self.__develop_command, shell=True)
        else:
            if self.__dockerfile_path is None and self.__docker_image is None:
                raise exceptions.ServiceException(
                    f'{self.get_name()} could not be executed. A Dockerfile or Docker image was not supplied. Check '
                    f'your "touchstone.yml".')
            docker_artifact = None
            log_path = None
            if self.__log_directory:
                log_path = os.path.join(self.__log_directory, f'{self.__name}.log')
            if self.__dockerfile_path is not None:
                self.__log('Building and running Dockerfile...')
                docker_artifact = self.__docker_manager.build_dockerfile(self.__dockerfile_path)
            if self.__docker_image is not None:
                self.__log('Running Docker image...')
                docker_artifact = self.__docker_image
            self.__docker_manager.run_foreground_image(docker_artifact, '"$(pwd)"/touchstone/io:/app/touchstone/io',
                                                       environment_vars, log_path, self.__docker_options)

    def __log(self, message: str):
        print(f'{self.get_name()} :: {message}')
