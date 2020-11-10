import os
from typing import Optional

from touchstone.lib.configs.service_config import ServiceConfig
from touchstone.lib.health_checks.blocking_health_check import BlockingHealthCheck
from touchstone.lib.health_checks.docker_health_check import DockerHealthCheck
from touchstone.lib.health_checks.http_health_check import HttpHealthCheck
from touchstone.lib.managers.docker_manager import DockerManager
from touchstone.lib.networking.docker_network import DockerNetwork
from touchstone.lib.services.executable_service import ExecutableService
from touchstone.lib.services.i_service import IService
from touchstone.lib.services.networked_service import NetworkedService
from touchstone.lib.tests import Tests


class ServiceFactory(object):
    def __init__(self, is_dev_mode: bool, root: str, docker_manager: DockerManager,
                 log_directory: Optional[str]):
        self.__is_dev_mode = is_dev_mode
        self.__root = root
        self.__docker_manager = docker_manager
        self.__log_directory = log_directory

    def get_service(self, service_config: ServiceConfig, tests: Tests) -> Optional[IService]:
        dockerfile_path = None
        if service_config.config['dockerfile']:
            dockerfile_path = os.path.abspath(os.path.join(self.__root, service_config.config['dockerfile']))
        service: Optional[IService] = None

        if service_config.config['type'] == 'networked':
            health_check = HttpHealthCheck() if service_config.config[
                                                    'availability_endpoint'] is not None else DockerHealthCheck()
            service = NetworkedService(service_config.config['name'],
                                       tests,
                                       dockerfile_path,
                                       service_config.config['docker_options'],
                                       self.__docker_manager,
                                       service_config.config['port'],
                                       service_config.config['availability_endpoint'],
                                       self.__log_directory,
                                       DockerNetwork(),
                                       health_check,
                                       BlockingHealthCheck(service_config.config['seconds_between_retries'],
                                                           service_config.config['num_retries'],
                                                           health_check))
        elif service_config.config['type'] == 'executable':
            service = ExecutableService(service_config.config['name'],
                                        self.__is_dev_mode,
                                        tests,
                                        dockerfile_path,
                                        service_config.config['docker_options'],
                                        self.__docker_manager,
                                        service_config.config['develop_command'],
                                        self.__log_directory)
        return service
