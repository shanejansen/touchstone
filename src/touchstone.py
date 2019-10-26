import sys
from multiprocessing.pool import ThreadPool

from pyfiglet import figlet_format

from docker_manager import DockerManager


class Touchstone(object):
    def __init__(self, services):
        self.services = services

    def run(self):
        print(figlet_format('Touchstone'))

        # TODO: read touchstone.json and start services

        thread_pool = ThreadPool(len(self.services))
        results = []
        try:
            for test_group in self.services:
                results.append(thread_pool.apply_async(lambda: test_group.run(), args=()))
            results = [r.get() for r in results]
            thread_pool.close()
            thread_pool.join()
        except:
            print('\nTouchstone tests were interrupted.')
            print('Cleaning up Docker images and containers.')
            self.__cleanup()
            raise

        if False in results:
            print('One or more Touchstone tests failed. Exiting...')
            self.__cleanup()
            sys.exit(1)
        else:
            print('All Touchstone tests passed successfully! Exiting...')
            self.__cleanup()
            sys.exit(0)

    @staticmethod
    def __cleanup():
        DockerManager.instance().cleanup()
