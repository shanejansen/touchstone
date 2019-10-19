import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from config import Config
from context.given_context import GivenContext
from context.then_context import ThenContext
from context.when_context import WhenContext


class Touchstone(object):
    def __init__(self, touchstone_tests, config=Config()):
        self.touchstone_tests = touchstone_tests
        self.given_context = GivenContext(config)
        self.when_context = WhenContext(config)
        self.then_context = ThenContext(config)

    def run(self):
        print('Running Touchstone tests...\n')
        self.wait_for_service_availability()
        for touchstone_test in self.touchstone_tests:
            test_name = touchstone_test.name()
            print(f'Running: {test_name}.')
            touchstone_test.given(self.given_context)
            test_result = touchstone_test.when(self.when_context)
            test_did_pass = touchstone_test.then(self.then_context, test_result)
            if not test_did_pass:
                print(f'FAILED - {test_name}. Exiting.')
                exit(1)
            else:
                print(f'PASSED - {test_name}.\n')
        print('Successfully ran all Touchstone tests.')

    def wait_for_service_availability(self):
        response = None
        for retry_num in range(self.when_context.config.num_retries):
            try:
                response = self.when_context.get_json(self.when_context.config.availability_endpoint)
            except urllib.error.URLError:
                print(
                    f'Service under test not available. Retry {retry_num + 1} of {self.when_context.config.num_retries}.')
                time.sleep(self.when_context.config.seconds_between_retries)
        if response is None:
            print(f'Could not connect to service after {self.when_context.config.num_retries} retries. Failing tests.')
            sys.exit(1)
