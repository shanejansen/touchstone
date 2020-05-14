import glob
import os
from pathlib import Path

import yaml

from touchstone.lib.configs.service_config import ServiceConfig
from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.mockables.networked_mock import NetworkedMock
from touchstone.lib.mocks.mocks import Mocks
from touchstone.lib.mocks.networked_runnables.http.http_runnable import HttpRunnable
from touchstone.lib.mocks.networked_runnables.mongodb.mongodb_runnable import MongodbRunnable
from touchstone.lib.mocks.networked_runnables.mysql.mysql_runnable import MysqlRunnable
from touchstone.lib.mocks.networked_runnables.rabbitmq.rabbitmq_runnable import RabbitmqRunnable
from touchstone.lib.mocks.networked_runnables.s3.s3_runnable import S3Runnable
from touchstone.lib.service import Service
from touchstone.lib.services import Services
from touchstone.lib.tests import Tests
from touchstone.runner import Runner


class Bootstrap(object):
    def __init__(self, is_dev_mode=False):
        self.is_dev_mode = is_dev_mode

        docker_manager = DockerManager(should_auto_discover=not self.is_dev_mode)
        touchstone_config = self.__build_touchstone_config(os.getcwd())
        self.runner = Runner(touchstone_config, docker_manager)
        self.mocks = self.__build_mocks(touchstone_config.config['root'],
                                        touchstone_config.config['mocks'],
                                        touchstone_config.config['host'], docker_manager)
        self.services = self.__build_services(touchstone_config.config['root'],
                                              touchstone_config.config['host'],
                                              touchstone_config.config['services'],
                                              docker_manager,
                                              self.mocks)

    def __build_touchstone_config(self, root) -> TouchstoneConfig:
        config = TouchstoneConfig(os.getcwd())
        path = os.path.join(root, 'touchstone.yml')
        with open(path, 'r') as file:
            config.merge(yaml.safe_load(file))
        return config

    def __build_mocks(self, root, configs, host, docker_manager) -> Mocks:
        defaults = {}
        default_files = glob.glob(os.path.join(root, 'defaults') + '/*.yml')
        for default_file in default_files:
            with open(default_file, 'r') as file:
                defaults[Path(default_file).stem] = yaml.safe_load(file)

        mocks = Mocks()
        for mock_name in configs:
            mock = None
            config = configs.get(mock_name, {})
            mock_defaults = defaults.get(mock_name, {})
            if mock_name == 'http':
                runnable = HttpRunnable(mock_defaults, docker_manager)
                mock = NetworkedMock('http', 'HTTP', host, runnable)
                mocks.http = runnable
            elif mock_name == 'rabbitmq':
                runnable = RabbitmqRunnable(mock_defaults, config, docker_manager)
                mock = NetworkedMock('rabbitmq', 'Rabbit MQ', host, runnable)
                mocks.rabbitmq = runnable
            elif mock_name == 'mongodb':
                runnable = MongodbRunnable(mock_defaults, self.is_dev_mode, docker_manager)
                mock = NetworkedMock('mongodb', 'Mongo DB', host, runnable)
                mocks.mongodb = runnable
            elif mock_name == 'mysql':
                runnable = MysqlRunnable(self.is_dev_mode, mock_defaults, config, docker_manager)
                mock = NetworkedMock('mysql', 'MySQL', host, runnable)
                mocks.mysql = runnable
            elif mock_name == 's3':
                base_objects_path = os.path.join(root, 'defaults')
                runnable = S3Runnable(mock_defaults, base_objects_path, docker_manager)
                mock = NetworkedMock('s3', 'S3', host, runnable)
                mocks.s3 = runnable
            if mock:
                mocks.register_mock(mock)
        return mocks

    def __build_services(self, root, host, user_service_configs, docker_manager, mocks) -> Services:
        services = []
        for given_service_config in user_service_configs:
            service_config = ServiceConfig(host)
            service_config.merge(given_service_config)
            tests_path = os.path.abspath(os.path.join(root, service_config.config['tests']))
            tests = Tests(mocks, tests_path)

            service = Service(root, service_config.config['name'], tests,
                              service_config.config['dockerfile'], service_config.config['host'],
                              service_config.config['port'], service_config.config['availability_endpoint'],
                              service_config.config['num_retries'], service_config.config['seconds_between_retries'],
                              docker_manager)

            services.append(service)
        return Services(services)
