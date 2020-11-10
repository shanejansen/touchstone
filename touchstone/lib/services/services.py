from typing import List, Tuple

from touchstone.lib import exceptions
from touchstone.lib.services.i_executable import IExecutable
from touchstone.lib.services.i_runnable import IRunnable
from touchstone.lib.services.i_service import IService
from touchstone.lib.services.i_service_executor import IServiceExecutor
from touchstone.lib.services.i_testable import ITestable


class Services(IServiceExecutor):
    def __init__(self):
        self.__services: List[IService] = []
        self.__services_running = False
        self.__environment_vars: List[Tuple[str, str]] = []

    def add_service(self, service: IService):
        self.__services.append(service)

    def add_environment_vars(self, environment_vars: List[Tuple[str, str]] = []):
        self.__environment_vars.extend(environment_vars)

    def start(self):
        if self.__services_running:
            print('Services have already been started. They cannot be started again.')
        else:
            runnables: List[IRunnable] = []
            for service in self.__services:
                if isinstance(service, IRunnable):
                    runnables.append(service)
            print(f'Starting services {[_.get_name() for _ in runnables]}...')
            for service in runnables:
                service.start(self.__environment_vars)
            self.__services_running = True
            for service in runnables:
                service.wait_until_healthy()
            print('Finished starting services.\n')

    def stop(self):
        print('Stopping services...')
        for service in self.__services:
            if isinstance(service, IRunnable):
                service.stop()
        self.__services_running = False

    def execute(self, service_name: str):
        found = False
        for service in self.__services:
            if service.get_name() == service_name and isinstance(service, IExecutable):
                found = True
                service.execute(self.__environment_vars)
        if not found:
            raise exceptions.ServiceException(f'Service could not be found with name: "{service_name}".')

    def run_test(self, service_name: str, file_name: str, test_name: str) -> bool:
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
