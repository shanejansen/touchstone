from typing import List

from touchstone.lib.mocks.run_context import RunContext
from touchstone.lib.service import Service


class Services(object):
    def __init__(self, services: List[Service]):
        self.__services = services
        self.__services_running = False

    def start(self, run_contexts: List[RunContext]):
        if self.__services_running:
            print('Services have already been started. They cannot be started again.')
        else:
            print(f'Starting services {[_.name for _ in self.__services]}...')
            for service in self.__services:
                service.start(run_contexts)
            self.__services_running = True
            for service in self.__services:
                service.wait_for_availability()
            print('Finished starting services.\n')

    def stop(self):
        print('Stopping services...')
        for service in self.__services:
            service.stop()
        self.__services_running = False

    def run_test(self, service_name, file_name, test_name) -> bool:
        found_service = None
        for service in self.__services:
            if service.name.replace(' ', '-').lower() == service_name:
                found_service = service
        if not found_service:
            print(f'No service could be found with the name "{service_name}".')
            return False

        return found_service.run_test(file_name, test_name)

    def run_all_tests(self) -> bool:
        for service in self.__services:
            did_pass = service.run_all_tests()
            if not did_pass:
                return False
        return True

    def are_running(self) -> bool:
        return self.__services_running
