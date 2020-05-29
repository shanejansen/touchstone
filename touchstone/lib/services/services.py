from typing import List, Tuple

from touchstone.lib.services.i_runnable import IRunnable
from touchstone.lib.services.i_service import IService
from touchstone.lib.services.i_testable import ITestable


class Services(object):
    def __init__(self, services: List[IService]):
        self.__services = services
        self.__services_running = False

    def start(self, environment_vars: List[Tuple[str, str]] = []):
        if self.__services_running:
            print('Services have already been started. They cannot be started again.')
        else:
            print(f'Starting services {[_.get_name() for _ in self.__services]}...')
            for service in self.__services:
                if isinstance(service, IRunnable):
                    service.start(environment_vars)
            self.__services_running = True
            for service in self.__services:
                if isinstance(service, IRunnable):
                    service.wait_for_availability()
            print('Finished starting services.\n')

    def stop(self):
        print('Stopping services...')
        for service in self.__services:
            if isinstance(service, IRunnable):
                service.stop()
        self.__services_running = False

    def run_test(self, service_name, file_name, test_name) -> bool:
        found_service = None
        for service in self.__services:
            if service.get_name().replace(' ', '-').lower() == service_name \
                    and isinstance(service, ITestable):
                found_service = service
        if not found_service:
            print(f'No testable service could be found with the name "{service_name}".')
            return False

        return found_service.run_test(file_name, test_name)

    def run_all_tests(self) -> bool:
        for service in self.__services:
            if isinstance(service, ITestable):
                did_pass = service.run_all_tests()
                if not did_pass:
                    return False
        return True

    def are_running(self) -> bool:
        return self.__services_running
