import glob
import os
import sys
from pathlib import Path

import yaml

from touchstone.lib import exceptions
from touchstone.lib.configs.service_config import ServiceConfig
from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.mock_factory import MockFactory
from touchstone.lib.mocks.mocks import Mocks
from touchstone.lib.services.networked_service import NetworkedService
from touchstone.lib.services.services import Services
from touchstone.lib.tests import Tests


class Bootstrap(object):
    def __init__(self, is_dev_mode=False):
        root = os.path.join(os.getcwd(), 'touchstone')
        touchstone_config = self.__build_touchstone_config(root)
        self.is_dev_mode = is_dev_mode
        self.docker_manager = DockerManager(should_auto_discover=not self.is_dev_mode)
        self.mocks = self.__build_mocks(touchstone_config.config['root'],
                                        touchstone_config.config['mocks'],
                                        touchstone_config.config['host'])
        self.services = self.__build_services(touchstone_config.config['root'],
                                              touchstone_config.config['host'],
                                              touchstone_config.config['services'],
                                              self.mocks)

    def __build_touchstone_config(self, root) -> TouchstoneConfig:
        config = TouchstoneConfig(root)
        path = os.path.join(root, 'touchstone.yml')
        with open(path, 'r') as file:
            config.merge(yaml.safe_load(file))
        return config

    def __build_mocks(self, root, configs, host) -> Mocks:
        defaults_paths = {}
        default_files = glob.glob(os.path.join(root, 'defaults') + '/*.yml')
        for default_file in default_files:
            defaults_paths[Path(default_file).stem] = default_file

        mocks = Mocks()
        for mock_name in configs:
            mock_factory = MockFactory(self.is_dev_mode, root, defaults_paths, configs, host, self.docker_manager)
            mock = mock_factory.get_mock(mock_name)
            if not mock:
                raise exceptions.MockNotSupportedException(f'Mock: {mock_name} is not supported.')
            setattr(mocks, mock_name, mock.get_runnable())
            mocks.register_mock(mock)
        return mocks

    def __build_services(self, root, host, user_service_configs, mocks) -> Services:
        services = []
        for given_service_config in user_service_configs:
            service_config = ServiceConfig(host)
            service_config.merge(given_service_config)
            tests_path = os.path.abspath(os.path.join(root, service_config.config['tests']))
            tests = Tests(mocks, tests_path)
            dockerfile_path = None
            if service_config.config['dockerfile']:
                dockerfile_path = os.path.abspath(os.path.join(root, service_config.config['dockerfile']))
            service = NetworkedService(service_config.config['name'], tests, dockerfile_path, self.docker_manager, host,
                                       service_config.config['port'], service_config.config['availability_endpoint'],
                                       service_config.config['num_retries'],
                                       service_config.config['seconds_between_retries'])
            services.append(service)
        return Services(services)

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
