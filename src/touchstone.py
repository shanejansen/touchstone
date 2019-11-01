import json
import os
import sys

from pyfiglet import figlet_format

from docker_manager import DockerManager
from mocks.mocks import Mocks
from touchstone_config import TouchstoneConfig


class Touchstone(object):
    def __init__(self, services, touchstone_config=os.path.abspath('./touchstone.json')):
        self.services = services
        self.results = None
        with open(touchstone_config, 'r') as file:
            TouchstoneConfig.instance().merge(json.load(file))

    def run(self):
        try:
            self.__run()
        except (Exception, KeyboardInterrupt) as e:
            print('\nTouchstone tests were interrupted. Cleaning up...')
            self.__cleanup()
            raise e

    def __run(self):
        print(figlet_format('Touchstone'))

        mocks = Mocks()
        mocks.start()
        self.results = self.__run_all_service_tests(mocks)

        if TouchstoneConfig.instance().config['dev'] is True:
            mocks.print_available_mocks()
            self.__accept_user_command()
        else:
            self.__exit()

    # Not threading for now since each mock is cleaned up after a test is ran
    def __run_all_service_tests(self, mocks):
        # thread_pool = ThreadPool(len(self.services))
        results = []
        for service in self.services:
            results.append(service.run(mocks))
            # results.append(thread_pool.apply_async(lambda: service.run(mocks)))
        # results = [r.get() for r in results]
        # thread_pool.close()
        # thread_pool.join()
        return results

    def __accept_user_command(self):
        print('\nAll Touchstone tests finished. In dev mode; keeping alive\n'
              'exit - Exit dev mode')
        while True:
            command = input('Touchstone Command: ')
            if command == 'exit':
                self.__exit()
            else:
                print(f'Unknown command "{command}"')

    def __exit(self):
        code = 0
        if self.results is None or False in self.results:
            print('One or more Touchstone tests failed. Exiting...')
            code = 1
        else:
            print('All Touchstone tests passed successfully! Exiting...')
        self.__cleanup()
        sys.exit(code)

    @staticmethod
    def __cleanup():
        DockerManager.instance().cleanup()
