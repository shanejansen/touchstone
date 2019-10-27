import sys
from multiprocessing.pool import ThreadPool

from pyfiglet import figlet_format

from docker_manager import DockerManager


class Touchstone(object):
    def __init__(self, services):
        self.services = services
        self.results = None

    def run(self):
        try:
            self.__run()
        except (Exception, KeyboardInterrupt) as e:
            print('\nTouchstone tests were interrupted. Cleaning up...')
            self.__cleanup()
            raise e

    def __run(self):
        print(figlet_format('Touchstone'))

        # TODO: read touchstone.json and start services
        self.results = self.__run_test_groups()

        if 'dev' in sys.argv:
            self.__accept_user_command()
        else:
            self.__exit()

    def __run_test_groups(self):
        thread_pool = ThreadPool(len(self.services))
        results = []
        for test_group in self.services:
            results.append(thread_pool.apply_async(lambda: test_group.run()))
        results = [r.get() for r in results]
        thread_pool.close()
        thread_pool.join()
        return results

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
