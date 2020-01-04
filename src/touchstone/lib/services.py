from typing import List

from touchstone.lib.service import Service


class Services(object):
    def __init__(self, services: List[Service]):
        self.__services = services
        self.__services_running = False

    def start(self):
        if self.__services_running:
            print('Services have already been started. They cannot be started again.')
        else:
            print(f'Starting services {[_.name for _ in self.__services]}...')
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
        try:
            self.__wait_for_availability()
        except KeyboardInterrupt:
            return False

        for service in self.__services:
            did_pass = service.run_tests()
            if not did_pass:
                return False
        return True

    def are_running(self) -> bool:
        return self.__services_running

    def __wait_for_availability(self):
        for service in self.__services:
            service.wait_for_availability()
