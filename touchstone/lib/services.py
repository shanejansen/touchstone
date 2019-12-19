import os

from touchstone.lib import exceptions
from touchstone.lib.configs.service_config import ServiceConfig
from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.mocks.mocks import Mocks
from touchstone.lib.service import Service
from touchstone.lib.tests import Tests


class Services(object):
    def __init__(self, mocks: Mocks):
        self.mocks: Mocks = mocks
        self.services: list = []

    def start(self):
        if self.services:
            raise exceptions.ServiceException('Services have already been started. They cannot be started again.')
        self.__parse_services()
        print(f'Starting services {[_.name() for _ in self.services]}...')
        for service in self.services:
            service.start()
        print('Finished starting services.\n')

    def stop(self):
        print('Stopping services...')
        for service in self.services:
            service.stop()
        self.services = []

    def run_tests(self) -> bool:
        self.__parse_services()
        for service in self.services:
            did_pass = service.run_tests()
            if not did_pass:
                return False
        return True

    def __parse_services(self):
        self.services = []
        for given_service_config in TouchstoneConfig.instance().config['services']:
            service_config = ServiceConfig()
            service_config.merge(given_service_config)
            tests_path = os.path.abspath(
                os.path.join(TouchstoneConfig.instance().config["root"], service_config.config["tests"]))
            tests = Tests(self.mocks, tests_path)
            service = Service(service_config, tests)
            self.services.append(service)
