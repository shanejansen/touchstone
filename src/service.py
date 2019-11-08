import http
import http.client
import time
import urllib.error
import urllib.parse
import urllib.request

from context.given_context import GivenContext
from context.then_context import ThenContext
from context.when_context import WhenContext
from docker_manager import DockerManager
from touchstone_config import TouchstoneConfig


class Service(object):
    def __init__(self, config, touchstone_tests):
        self.config = config
        self.touchstone_tests = touchstone_tests

    def run(self, mocks):
        given_context = GivenContext(self.config, mocks)
        when_context = WhenContext(self.config, mocks)
        then_context = ThenContext(self.config, mocks)

        if TouchstoneConfig.instance().config['dev'] is False and self.config.service_dockerfile is not None:
            self.__log('Building and running Dockerfile...')
            tag = DockerManager.instance().build_dockerfile(self.config.service_dockerfile)
            DockerManager.instance().run_image(tag, self.config.service_exposed_port,
                                               self.config.service_port)

        if self.__wait_for_availability(when_context) is False:
            self.__log('FAILED - Could not connect to service\'s availability endpoint.\n')
            return False

        return self.__run_tests(mocks, given_context, when_context, then_context)

    def __log(self, message):
        print(f'{self.config.service_host} :: {message}')

    def __wait_for_availability(self, when_context):
        response = None
        full_endpoint = self.config.service_url + self.config.service_availability_endpoint
        self.__log(f'Attempting to connect to availability endpoint {full_endpoint}')
        for retry_num in range(self.config.num_retries):
            try:
                response = when_context.get_text(self.config.service_availability_endpoint)
                return True
            except (urllib.error.URLError, http.client.RemoteDisconnected):
                self.__log(f'Not available. Retry {retry_num + 1} of {self.config.num_retries}.')
                time.sleep(self.config.seconds_between_retries)
        if response is None:
            return False
        return True

    def __run_tests(self, mocks, given_context, when_context, then_context):
        tests_passed = True
        for touchstone_test in self.touchstone_tests:
            test_name = touchstone_test.name()
            self.__log(f'RUNNING -  {test_name}.')
            touchstone_test.given(given_context)
            test_result = touchstone_test.when(when_context)
            test_did_pass = touchstone_test.then(then_context, test_result)
            if not test_did_pass:
                self.__log(f'FAILED - {test_name}. Unexpected value "{test_result}"\n')
                tests_passed = False
            else:
                self.__log(f'PASSED - {test_name}.\n')
            mocks.cleanup()
        return tests_passed
