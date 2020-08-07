import subprocess
from typing import List, Tuple

from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.services.i_executable import IExecutable
from touchstone.lib.services.i_service import IService
from touchstone.lib.services.i_testable import ITestable
from touchstone.lib.tests import Tests


class ExecutableService(IService, ITestable, IExecutable):
    def __init__(self, name: str, is_dev_mode: bool, tests: Tests, dockerfile_path: str, docker_manager: DockerManager,
                 develop_command: str):
        self.__name = name
        self.__is_dev_mode = is_dev_mode
        self.__tests = tests
        self.__dockerfile_path = dockerfile_path
        self.__docker_manager = docker_manager
        self.__develop_command = develop_command

    def get_name(self):
        return self.__name

    def run_test(self, file_name, test_name) -> bool:
        return self.__tests.run(file_name, test_name)

    def run_all_tests(self) -> bool:
        self.__log('Running all tests...')
        did_pass = self.__tests.run_all()
        self.__log('Finished running all tests.\n')
        return did_pass

    def execute(self, environment_vars: List[Tuple[str, str]] = []):
        if self.__is_dev_mode:
            subprocess.run(self.__develop_command, shell=True)
        else:
            if self.__dockerfile_path is not None:
                self.__log('Building and running Dockerfile...')
                tag = self.__docker_manager.build_dockerfile(self.__dockerfile_path)
                self.__docker_manager.run_foreground_image(tag, '"$(pwd)"/touchstone/io:/app/touchstone/io',
                                                           environment_vars)
            else:
                self.__log('Service could not be executed. A Dockerfile was not supplied. Check your "touchstone.yml".')

    def __log(self, message: str):
        print(f'{self.get_name()} :: {message}')