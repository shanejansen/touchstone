import json
import os
import sys

from pyfiglet import figlet_format

from docker_manager import DockerManager
from mocks.mocks import Mocks
from touchstone_config import TouchstoneConfig


class Touchstone(object):
    def __init__(self, services, root=os.path.abspath('./')):
        self.services = services
        TouchstoneConfig.instance().set_root(root)
        with open(os.path.join(TouchstoneConfig.instance().config['root'], 'touchstone.json'), 'r') as file:
            TouchstoneConfig.instance().merge(json.load(file))

    def run(self):
        try:
            self.__run()
        except (Exception, KeyboardInterrupt) as e:
            print('\nTouchstone tests were interrupted. Cleaning up...')
            DockerManager.instance().cleanup()
            raise e

    def __run(self):
        print(figlet_format('Touchstone'))

        mocks = Mocks()
        mocks.start()

        if TouchstoneConfig.instance().config['dev'] is True:
            mocks.load_defaults()
            mocks.print_available_mocks()
            self.__accept_user_command()
        else:
            results = self.__run_all_service_tests(mocks)
            if False in results:
                print('One or more Touchstone tests failed. Exiting...')
                self.__exit(False)
            else:
                print('All Touchstone tests passed successfully! Exiting...')
                self.__exit(True)

    def __run_all_service_tests(self, mocks):
        results = []
        for service in self.services:
            results.append(service.run(mocks))
        return results

    def __accept_user_command(self):
        print('\nIn dev mode - keeping alive\n'
              'exit - Exit dev mode')
        while True:
            command = input('Touchstone Command: ')
            if command == 'exit':
                print('Exiting...')
                self.__exit(True)
            else:
                print(f'Unknown command "{command}"')

    def __exit(self, did_pass):
        if did_pass:
            code = 0
        else:
            code = 1
        DockerManager.instance().cleanup()
        sys.exit(code)
