import glob
import os

import yaml

from touchstone.lib.configs.service_config import ServiceConfig
from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.mocks import Mocks
from touchstone.lib.service import Service
from touchstone.lib.services import Services
from touchstone.lib.tests import Tests
from touchstone.runner import Runner


class Bootstrap(object):
    def __init__(self, is_dev_mode=False):
        self.is_dev_mode = is_dev_mode

        docker_manager = DockerManager(should_auto_discover=not self.is_dev_mode)
        self.touchstone_config = self.__build_touchstone_config(os.getcwd())
        self.runner = Runner(self.touchstone_config, docker_manager)
        self.mocks = self.__build_mocks(self.touchstone_config.config['root'], self.touchstone_config,
                                        self.touchstone_config.config['host'], docker_manager)
        self.services = self.__build_services(self.touchstone_config, docker_manager, self.mocks)

    def __build_touchstone_config(self, root) -> TouchstoneConfig:
        config = TouchstoneConfig(os.getcwd())
        path = os.path.join(root, 'touchstone.yml')
        with open(path, 'r') as file:
            config.merge(yaml.safe_load(file))
        return config

    def __build_mocks(self, root, touchstone_config, host, docker_manager) -> Mocks:
        defaults = {}
        default_files = glob.glob(os.path.join(root, 'defaults') + '/*.yml')
        for default_file in default_files:
            with open(default_file, 'r') as file:
                defaults[file.name] = yaml.safe_load(file)

        mocks = Mocks()
        mocks.register_mocks(touchstone_config.config['mocks'], defaults, docker_manager, host)
        return mocks

    def __build_services(self, touchstone_config, docker_manager, mocks) -> Services:
        services = []
        for given_service_config in touchstone_config.config['services']:
            service_config = ServiceConfig(touchstone_config.config['host'])
            service_config.merge(given_service_config)
            tests_path = os.path.abspath(
                os.path.join(touchstone_config.config['root'], service_config.config['tests']))
            tests = Tests(mocks, tests_path)

            service = Service(touchstone_config.config['root'], service_config.config['name'], tests,
                              service_config.config['dockerfile'], service_config.config['host'],
                              service_config.config['port'], service_config.config['availability_endpoint'],
                              service_config.config['num_retries'], service_config.config['seconds_between_retries'],
                              docker_manager)

            services.append(service)
        return Services(services)
