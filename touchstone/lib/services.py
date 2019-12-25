import os

from touchstone.lib.configs.service_config import ServiceConfig
from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.mocks.mocks import Mocks
from touchstone.lib.service import Service
from touchstone.lib.tests import Tests


class Services(object):
    def __init__(self, mocks: Mocks):
        self.__mocks: Mocks = mocks
        self.__services: list = self.__parse_services()
        self.__services_running = False

    def start(self):
        if self.__services_running:
            print('Services have already been started. They cannot be started again.')
        else:
            print(f'Starting services {[_.name() for _ in self.__services]}...')
            for service in self.__services:
                service.start()
            self.__services_running = True
            print('Finished starting services.\n')

    def stop(self):
        print('Stopping services...')
        for service in self.__services:
            service.stop()
        self.__services_running = False

    def run_tests(self) -> bool:
        for service in self.__services:
            did_pass = service.run_tests()
            if not did_pass:
                return False
        return True

    def __parse_services(self) -> list:
        services = []
        for given_service_config in TouchstoneConfig.instance().config['services']:
            service_config = ServiceConfig()
            service_config.merge(given_service_config)
            tests_path = os.path.abspath(
                os.path.join(TouchstoneConfig.instance().config['root'], service_config.config['tests']))
            tests = Tests(self.__mocks, tests_path)
            service = Service(service_config, tests)
            services.append(service)
        return services
