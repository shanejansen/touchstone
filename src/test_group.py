import time
import urllib.error
import urllib.parse
import urllib.request

from context.given_context import GivenContext
from context.then_context import ThenContext
from context.when_context import WhenContext


class TestGroup(object):
    def __init__(self, config, touchstone_tests):
        self.config = config
        self.touchstone_tests = touchstone_tests
        self.given_context = GivenContext(config)
        self.when_context = WhenContext(config)
        self.then_context = ThenContext(config)
        self.group_name = self.config.service_host
        self.did_pass = True

    def run(self):
        if self.wait_for_service_availability() is False:
            print(
                f'{self.group_name} :: FAILED - Could not connect to service\'s availability endpoint.\n')
            return False

        for touchstone_test in self.touchstone_tests:
            test_name = touchstone_test.name()
            print(f'{self.group_name} :: RUNNING -  {test_name}.')
            touchstone_test.given(self.given_context)
            test_result = touchstone_test.when(self.when_context)
            test_did_pass = touchstone_test.then(self.then_context, test_result)
            if not test_did_pass:
                print(f'{self.group_name} :: FAILED - {test_name}. Unexpected value "{test_result}"\n')
                self.did_pass = False
            else:
                print(f'{self.group_name} :: PASSED - {test_name}.\n')

        return self.did_pass

    def wait_for_service_availability(self):
        response = None
        full_endpoint = self.config.service_url + self.config.service_availability_endpoint
        print(f'{self.group_name} :: Attempting to connect to availability endpoint {full_endpoint}')
        for retry_num in range(self.config.num_retries):
            try:
                response = self.when_context.get_text(self.config.service_availability_endpoint)
                return True
            except urllib.error.URLError:
                print(
                    f'{self.group_name} not available. Retry {retry_num + 1} of {self.config.num_retries}.')
                time.sleep(self.config.seconds_between_retries)
        if response is None:
            return False
        return True
