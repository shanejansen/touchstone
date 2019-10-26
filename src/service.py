import time
import urllib.error
import urllib.parse
import urllib.request

from context.given_context import GivenContext
from context.then_context import ThenContext
from context.when_context import WhenContext
from docker_manager import DockerManager


class Service(object):
    def __init__(self, config, touchstone_tests):
        self.config = config
        self.touchstone_tests = touchstone_tests
        self.given_context = GivenContext(config)
        self.when_context = WhenContext(config)
        self.then_context = ThenContext(config)

    def run(self):
        if self.config.service_dockerfile is not None:
            tag = DockerManager.instance().build_dockerfile(self.config.service_dockerfile)
            host_port = DockerManager.instance().run_image(tag, port=self.config.service_port)

        if self.__wait_for_availability() is False:
            print(self.__log('FAILED - Could not connect to service\'s availability endpoint.\n'))
            return False
        return self.__run_tests()

    def __log(self, message):
        print(f'{self.config.service_host} :: {message}')

    def __wait_for_availability(self):
        response = None
        full_endpoint = self.config.service_url + self.config.service_availability_endpoint
        print(f'\nAttempting to connect to availability endpoint {full_endpoint}')
        for retry_num in range(self.config.num_retries):
            try:
                response = self.when_context.get_text(self.config.service_availability_endpoint)
                return True
            except urllib.error.URLError:
                self.__log(f'Not available. Retry {retry_num + 1} of {self.config.num_retries}.')
                time.sleep(self.config.seconds_between_retries)
        if response is None:
            return False
        return True

    def __run_tests(self):
        tests_passed = True
        for touchstone_test in self.touchstone_tests:
            test_name = touchstone_test.name()
            self.__log(f'RUNNING -  {test_name}.')
            touchstone_test.given(self.given_context)
            test_result = touchstone_test.when(self.when_context)
            test_did_pass = touchstone_test.then(self.then_context, test_result)
            if not test_did_pass:
                self.__log(f'FAILED - {test_name}. Unexpected value "{test_result}"\n')
                tests_passed = False
            else:
                self.__log(f'PASSED - {test_name}.\n')
        return tests_passed
