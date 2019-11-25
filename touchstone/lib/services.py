import os

from lib.configs.service_config import ServiceConfig
from lib.configs.touchstone_config import TouchstoneConfig
from lib.mocks.mocks import Mocks
from lib.service import Service
from lib.tests import Tests


class Services(object):
    def __init__(self, mocks: Mocks):
        self.mocks = mocks
        self.services: list = []

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
            tests_path = os.path.join(TouchstoneConfig.instance().config["root"], service_config.config["tests"])
            tests = Tests(self.mocks, tests_path)
            service = Service(service_config, tests)
            self.services.append(service)
