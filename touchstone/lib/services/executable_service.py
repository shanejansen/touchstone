import subprocess

from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.services.i_executable import IExecutable
from touchstone.lib.services.i_service import IService
from touchstone.lib.services.i_testable import ITestable
from touchstone.lib.tests import Tests


class ExecutableService(IService, ITestable, IExecutable):
    def __init__(self, name: str, is_dev_mode: bool, tests: Tests, dockerfile_path: str, docker_manager: DockerManager,
                 execute_command: str):
        self.__name = name
        self.__is_dev_mode = is_dev_mode
        self.__tests = tests
        self.__dockerfile_path = dockerfile_path
        self.__docker_manager = docker_manager
        self.__execute_command = execute_command

    def get_name(self):
        return self.__name

    def run_test(self, file_name, test_name) -> bool:
        return self.__tests.run(file_name, test_name)

    def run_all_tests(self) -> bool:
        self.__log('Running all tests...')
        did_pass = self.__tests.run_all()
        self.__log('Finished running all tests.\n')
        return did_pass

    def execute(self):
        if not self.__is_dev_mode:
            if self.__dockerfile_path is not None:
                self.__log('Building and running Dockerfile...')
                tag = self.__docker_manager.build_dockerfile(self.__dockerfile_path)
                self.__docker_manager.run_image(tag)
            else:
                self.__log('Service could not be executed. A Dockerfile was not supplied. Check your "touchstone.yml".')
        else:
            subprocess.run(self.__execute_command, shell=True)

    def __log(self, message: str):
        print(f'{self.get_name()} :: {message}')
