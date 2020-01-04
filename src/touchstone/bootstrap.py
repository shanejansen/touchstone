import os

import yaml

from touchstone import common
from touchstone.lib import exceptions
from touchstone.lib.configs.service_config import ServiceConfig
from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.http.http import Http
from touchstone.lib.mocks.mocks import Mocks
from touchstone.lib.mocks.mongodb.mongodb import Mongodb
from touchstone.lib.mocks.rabbitmq.rabbitmq import Rabbitmq
from touchstone.lib.service import Service
from touchstone.lib.services import Services
from touchstone.lib.tests import Tests
from touchstone.runner import Runner


class Bootstrap(object):
    def __init__(self):
        docker_manager = DockerManager()

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

    def __build_mocks(self, root, touchstone_config, default_host, docker_manager) -> Mocks:
        http = None
        rabbitmq = None
        mongodb = None
        for mock in touchstone_config.config['mocks']:
            user_config = touchstone_config.config['mocks'][mock]
            if Http.name() == mock:
                http = Http(default_host, docker_manager)
                http.config = common.dict_merge(http.default_config(), user_config)
            elif Rabbitmq.name() == mock:
                rabbitmq = Rabbitmq(default_host, docker_manager)
                rabbitmq.config = common.dict_merge(rabbitmq.default_config(), user_config)
            elif Mongodb.name() == mock:
                mongodb = Mongodb(default_host, docker_manager)
                mongodb.config = common.dict_merge(mongodb.default_config(), user_config)
            else:
                raise exceptions.MockNotSupportedException(
                    f'{mock} is not a supported mock. Please check your touchstone.yml file.')
        return Mocks(root, http, rabbitmq, mongodb)

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
