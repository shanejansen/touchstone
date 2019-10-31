import json
import os
import sys
from multiprocessing.pool import ThreadPool

from pyfiglet import figlet_format

from docker_manager import DockerManager
from mocks.mocks import Mocks


class Touchstone(object):
    def __init__(self, services, touchstone_config=os.path.abspath('./touchstone.json')):
        self.services = services
        self.results = None
        with open(touchstone_config, 'r') as file:
            self.touchstone_config = self.__parse_touchstone_config(json.load(file))

    def run(self):
        try:
            self.__run()
        except (Exception, KeyboardInterrupt) as e:
            print('\nTouchstone tests were interrupted. Cleaning up...')
            self.__cleanup()
            raise e

    def __run(self):
        print(figlet_format('Touchstone'))

        mocks = Mocks(self.touchstone_config)
        mocks.start()
        self.results = self.__run_test_groups(mocks)

        if self.touchstone_config['dev'] is True:
            self.__accept_user_command()
        else:
            self.__exit()

    def __run_test_groups(self, mocks):
        thread_pool = ThreadPool(len(self.services))
        results = []
        for test_group in self.services:
            results.append(thread_pool.apply_async(lambda: test_group.run(mocks)))
        results = [r.get() for r in results]
        thread_pool.close()
        thread_pool.join()
        return results

    def __parse_touchstone_config(self, touchstone_config):
        dev = False
        if 'dev' in touchstone_config:
            dev = True if touchstone_config['dev'] == 'true' else False
        touchstone_config['dev'] = dev
        return touchstone_config

    def __accept_user_command(self):
        print('All Touchstone tests finished. In dev mode; keeping alive\n'
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
