import glob
import importlib.util
import inspect
from typing import Optional

from touchstone.lib import exceptions
from touchstone.lib.mocks.mocks import Mocks
from touchstone.lib.test import TestContainer, TestClass


class Tests(object):
    def __init__(self, mocks: Mocks, tests_path: str):
        self.service_url: Optional[str] = None
        self.__mocks = mocks
        self.__tests_path = tests_path

    def run(self, file_name, test_name) -> bool:
        if not self.service_url:
            raise exceptions.TestException('service_url must be set before running tests.')
        test_container = self.__load_test_class(file_name, test_name)

        if not test_container:
            print(f'No tests found with file name "{file_name}".')
            return False
        return test_container.execute(self.service_url, self.__mocks)

    def run_all(self) -> bool:
        if not self.service_url:
            raise exceptions.TestException('service_url must be set before running tests.')
        all_test_containers = self.__load_test_classes()
        if len(all_test_containers) == 0:
            print(f'No tests found at {self.__tests_path}')
            return False

        tests_passed = True
        for test_container in all_test_containers:
            print(test_container.file)
            if not test_container.execute(self.service_url, self.__mocks):
                tests_passed = False

        self.__mocks.load_defaults()
        return tests_passed

    def __load_test_class(self, file_name, test_name):
        file = glob.glob(f'{self.__tests_path}/{file_name}.py')
        if len(file) == 0:
            return None
        file = file[0]
        test_container = TestContainer(file)

        spec = importlib.util.spec_from_file_location(file, file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        members = [o for o in inspect.getmembers(module) if inspect.isclass(o[1])]
        for member in members:
            class_name = member[0]
            class_type = member[1]
            if class_name.lower() == test_name and module.__file__ == class_type.__module__:
                test_class = TestClass(class_name, class_type)
                test_container.add_test_class(test_class)
        return test_container

    def __load_test_classes(self):
        files = glob.glob(f'{self.__tests_path}/*.py')
        all_test_containers = []
        for file in files:
            test_container = TestContainer(file)
            all_test_containers.append(test_container)

            spec = importlib.util.spec_from_file_location(file, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            members = [o for o in inspect.getmembers(module) if inspect.isclass(o[1])]
            for member in members:
                class_name = member[0]
                class_type = member[1]
                if module.__file__ == class_type.__module__:
                    test_class = TestClass(class_name, class_type)
                    test_container.add_test_class(test_class)
        return all_test_containers
