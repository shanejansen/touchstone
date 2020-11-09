import glob
import os
import sys
from pathlib import Path

import yaml

from touchstone.lib import exceptions
from touchstone.lib.configs.service_config import ServiceConfig
from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.managers.docker_manager import DockerManager
from touchstone.lib.mocks.mock_factory import MockFactory
from touchstone.lib.mocks.mocks import Mocks
from touchstone.lib.services.service_factory import ServiceFactory
from touchstone.lib.services.services import Services
from touchstone.lib.tests import Tests


class Bootstrap(object):
    def __init__(self, is_dev_mode=False, should_log_services=False):
        root = os.path.join(os.getcwd(), 'touchstone')
        touchstone_config = self.__build_touchstone_config(root)
        log_directory = None
        if should_log_services:
            log_directory = os.path.join(root, 'logs')
            os.makedirs(log_directory, exist_ok=True)
        self.docker_manager = DockerManager(should_auto_discover=not is_dev_mode)
        self.mocks = self.__build_mocks(is_dev_mode,
                                        touchstone_config.config['root'],
                                        touchstone_config.config['mocks'])
        self.services = self.__build_services(is_dev_mode,
                                              touchstone_config.config['root'],
                                              touchstone_config.config['services'],
                                              self.mocks, log_directory)

    def __build_touchstone_config(self, root) -> TouchstoneConfig:
        config = TouchstoneConfig(root)
        path = os.path.join(root, 'touchstone.yml')
        with open(path, 'r') as file:
            config.merge(yaml.safe_load(file))
        return config

    def __build_mocks(self, is_dev_mode, root, configs) -> Mocks:
        defaults_paths = {}
        default_files = glob.glob(os.path.join(root, 'defaults') + '/*.yml')
        for default_file in default_files:
            defaults_paths[Path(default_file).stem] = default_file

        mocks = Mocks()
        mock_factory = MockFactory(is_dev_mode, root, defaults_paths, configs, self.docker_manager)
        for mock_name in configs:
            mock = mock_factory.get_mock(mock_name)
            if not mock:
                raise exceptions.MockNotSupportedException(f'Mock: {mock_name} is not supported.')
            setattr(mocks, mock_name, mock.get_runnable())
            mocks.register_mock(mock)
        return mocks

    def __build_services(self, is_dev_mode, root, user_service_configs, mocks, log_directory) -> Services:
        services = Services()
        service_factory = ServiceFactory(is_dev_mode, root, self.docker_manager, log_directory)
        for user_service_config in user_service_configs:
            service_config = ServiceConfig()
            service_config.merge(user_service_config)
            tests_path = os.path.abspath(os.path.join(root, service_config.config['tests']))
            tests = Tests(mocks, services, tests_path)
            service = service_factory.get_service(service_config, tests)
            services.add_service(service)
        return services

    def cleanup(self):
        self.services.stop()
        self.mocks.stop()
        self.docker_manager.cleanup()

    def exit(self, is_successful: bool):
        print('Shutting down...')
        if is_successful:
            code = 0
        else:
            code = 1
        self.cleanup()
        sys.exit(code)
