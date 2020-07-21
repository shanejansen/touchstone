import os
from typing import Optional

from touchstone.lib.configs.service_config import ServiceConfig
from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.services.executable_service import ExecutableService
from touchstone.lib.services.i_service import IService
from touchstone.lib.services.networked_service import NetworkedService
from touchstone.lib.tests import Tests


class ServiceFactory(object):
    def __init__(self, is_dev_mode: bool, root: str, docker_manager: DockerManager):
        self.__is_dev_mode = is_dev_mode
        self.__root = root
        self.__docker_manager = docker_manager

    def get_service(self, service_config: ServiceConfig, tests: Tests) -> Optional[IService]:
        dockerfile_path = None
        if service_config.config['dockerfile']:
            dockerfile_path = os.path.abspath(os.path.join(self.__root, service_config.config['dockerfile']))
        service: Optional[IService] = None

        if service_config.config['type'] == 'networked':
            service = NetworkedService(service_config.config['name'], tests, dockerfile_path, self.__docker_manager,
                                       service_config.config['host'], service_config.config['port'],
                                       service_config.config['availability_endpoint'],
                                       service_config.config['num_retries'],
                                       service_config.config['seconds_between_retries'])
        elif service_config.config['type'] == 'executable':
            service = ExecutableService(service_config.config['name'], self.__is_dev_mode, tests, dockerfile_path,
                                        self.__docker_manager, service_config.config['execute_command'])

        return service
