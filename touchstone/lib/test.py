import time
import traceback
from typing import List

from touchstone.lib.mocks.mocks import Mocks
from touchstone.lib.services.i_service_executor import IServiceExecutor
from touchstone.lib.touchstone_test import TouchstoneTest


class TestClass(object):
    def __init__(self, name, clazz):
        self.name = name
        self.clazz = clazz


class TestContainer(object):
    def __init__(self, file):
        self.file = file
        self.test_classes: List[TestClass] = []

    def add_test_class(self, test_class: TestClass):
        self.test_classes.append(test_class)

    def execute(self, service_url: str, mocks: Mocks, service_executor: IServiceExecutor) -> bool:
        all_passed = True
        for test_class in self.test_classes:
            class_instance: TouchstoneTest = test_class.clazz(service_url, mocks, service_executor)
            test = Test(test_class.name, class_instance)
            print(f'{test.name} :: RUNNING')
            mocks.reset()

            did_pass = False
            try:
                did_pass = test.run()
            except Exception:
                traceback.print_exc()
                all_passed = False

            if not did_pass:
                print(f'{test.name} :: FAILED\n')
                all_passed = False
            else:
                print(f'{test.name} :: PASSED\n')
        return all_passed


class Test(object):
    def __init__(self, name: str, touchstone_test: TouchstoneTest):
        self.name = name
        self.__touchstone_test = touchstone_test

    def run(self) -> bool:
        given = self.__touchstone_test.given()
        result = self.__touchstone_test.when(given)
        time.sleep(self.__touchstone_test.processing_period())
        did_pass = self.__touchstone_test.then(given, result)
        return did_pass
