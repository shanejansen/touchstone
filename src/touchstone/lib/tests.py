import glob
import importlib.util
import inspect
import traceback
from typing import Optional

from touchstone.lib import exceptions
from touchstone.lib.mocks.mocks import Mocks
from touchstone.lib.test import Test
from touchstone.lib.touchstone_test import TouchstoneTest


class Tests(object):
    def __init__(self, mocks: Mocks, tests_path: str):
        self.service_url: Optional[str] = None
        self.__mocks = mocks
        self.__tests_path = tests_path

    class TestContainer(object):
        def __init__(self, file):
            self.file = file
            self.test_classes = []

        def add_test_class(self, test_class):
            self.test_classes.append(test_class)

    class TestClass(object):
        def __init__(self, name, clazz):
            self.name = name
            self.clazz = clazz

    def run(self) -> bool:
        if not self.service_url:
            raise exceptions.TestException('service_url must be set before running tests.')

        all_test_containers = self.__load_test_classes()
        if len(all_test_containers) == 0:
            print(f'No tests found at {self.__tests_path}')
            return False

        tests_passed = True
        for test_container in all_test_containers:
            print(test_container.file)
            for test_class in test_container.test_classes:
                class_instance: TouchstoneTest = test_class.clazz(self.service_url, self.__mocks)
                test = Test(test_class.name, class_instance)
                print(f'{test.name} :: RUNNING')

                did_pass = False
                try:
                    did_pass = test.run()
                except Exception:
                    traceback.print_exc()
                    tests_passed = False

                if not did_pass:
                    print(f'{test.name} :: FAILED\n')
                    tests_passed = False
                else:
                    print(f'{test.name} :: PASSED\n')
                self.__mocks.reset()
        return tests_passed

    def __load_test_classes(self):
        files = glob.glob(f'{self.__tests_path}/*.py')
        all_test_containers = []
        for file in files:
            test_container = self.TestContainer(file)
            all_test_containers.append(test_container)

            spec = importlib.util.spec_from_file_location(file, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            members = [o for o in inspect.getmembers(module) if inspect.isclass(o[1])]
            for member in members:
                class_name = member[0]
                class_type = member[1]
                if module.__file__ == class_type.__module__:
                    test_class = self.TestClass(class_name, class_type)
                    test_container.add_test_class(test_class)
        return all_test_containers
