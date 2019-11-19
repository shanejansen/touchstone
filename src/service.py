import http
import http.client
import time
import urllib.error
import urllib.parse
import urllib.request

from configs.service_config import Config
from configs.touchstone_config import TouchstoneConfig
from docker_manager import DockerManager
from mocks.mocks import Mocks
from test_context import TestContext


class Service(object):
    def __init__(self, config: Config, touchstone_tests):
        self.config = config
        self.touchstone_tests = touchstone_tests

    def run_tests(self, mocks: Mocks) -> bool:
        test_context = TestContext(self.config, mocks)

        if TouchstoneConfig.instance().config['dev'] is False and self.config.service_dockerfile is not None:
            self.__log('Building and running Dockerfile...')
            tag = DockerManager.instance().build_dockerfile(self.config.service_dockerfile)
            DockerManager.instance().run_image(tag, self.config.service_exposed_port,
                                               self.config.service_port)

        if self.__wait_for_availability() is False:
            self.__log('FAILED - Could not connect to service\'s availability endpoint.\n')
            return False

        return self.__run_tests(mocks, test_context)

    def __wait_for_availability(self) -> bool:
        response = None
        full_endpoint = self.config.service_url + self.config.service_availability_endpoint
        self.__log(f'Attempting to connect to availability endpoint {full_endpoint}')
        for retry_num in range(self.config.num_retries):
            try:
                response = urllib.request.urlopen(full_endpoint).read()
                return True
            except (urllib.error.URLError, http.client.RemoteDisconnected):
                self.__log(f'Not available. Retry {retry_num + 1} of {self.config.num_retries}.')
                time.sleep(self.config.seconds_between_retries)
        if response is None:
            return False
        return True

    def __run_tests(self, mocks: Mocks, test_context: TestContext):
        tests_passed = True
        for touchstone_test in self.touchstone_tests:
            test_name = touchstone_test.name()
            self.__log(f'RUNNING -  {test_name}.')
            touchstone_test.given(test_context)
            test_result = touchstone_test.when(test_context)
            test_did_pass = touchstone_test.then(test_context, test_result)
            if not test_did_pass:
                self.__log(f'FAILED - {test_name}. Unexpected value "{test_result}"\n')
                tests_passed = False
            else:
                self.__log(f'PASSED - {test_name}.\n')
            mocks.cleanup()
        return tests_passed

    def __log(self, message: str):
        print(f'{self.config.service_host} :: {message}')
