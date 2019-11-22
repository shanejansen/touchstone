from configs.service_config import ServiceConfig
from configs.touchstone_config import TouchstoneConfig
from mocks.mocks import Mocks
from service import Service
from tests import Tests


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
            tests_path = f'{TouchstoneConfig.instance().config["root"]}/{service_config.config["tests"]}'
            tests = Tests(self.mocks, tests_path)
            service = Service(service_config, tests)
            self.services.append(service)
