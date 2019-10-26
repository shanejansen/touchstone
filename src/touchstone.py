import sys
from multiprocessing.pool import ThreadPool

from pyfiglet import figlet_format


class Touchstone(object):
    def __init__(self, test_groups):
        self.test_groups = test_groups

    def run(self):
        print(figlet_format('Touchstone'))
        thread_pool = ThreadPool(len(self.test_groups))
        results = []
        for test_group in self.test_groups:
            results.append(thread_pool.apply_async(lambda: test_group.run(), args=()))
        results = [r.get() for r in results]
        thread_pool.close()
        thread_pool.join()

        if False in results:
            print('One or more Touchstone tests failed.')
            sys.exit(1)
        else:
            print('All Touchstone tests passed successfully!')
            sys.exit(0)
