import glob
import importlib.util
import inspect
import os
import sys

from touchstone.lib.mocks.mocks import Mocks
from touchstone.lib.services.i_service_executor import IServiceExecutor
from touchstone.lib.test import TestContainer, TestClass


class Tests(object):
    __TEST_PREFIX = 'test_'

    def __init__(self, mocks: Mocks, service_executor: IServiceExecutor, tests_path: str):
        self.__mocks = mocks
        self.__service_executor = service_executor
        self.__tests_path = tests_path

    def run(self, file_name: str, test_name: str, service_url: str = None) -> bool:
        self.__load_package(self.__tests_path)
        self.__reload_support_modules(self.__tests_path)
        test_container = self.__load_test_class(file_name, test_name)

        if not test_container:
            print(f'No tests found with file name "{file_name}".')
            return False
        return test_container.execute(service_url, self.__mocks, self.__service_executor)

    def run_all(self, service_url: str = None) -> bool:
        self.__load_package(self.__tests_path)
        self.__reload_support_modules(self.__tests_path)
        all_test_containers = self.__load_test_classes()
        if len(all_test_containers) == 0:
            print(f'No tests found at {self.__tests_path}')
            return False

        tests_passed = True
        for test_container in all_test_containers:
            print(f'\n{test_container.file}')
            if not test_container.execute(service_url, self.__mocks, self.__service_executor):
                tests_passed = False

        self.__mocks.reset()
        return tests_passed

    def __load_module(self, name: str, path):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module

    def __load_package(self, path: str):
        module_name = os.path.basename(path)
        init_path = os.path.join(path, '__init__.py')
        self.__load_module(module_name, init_path)

    def __reload_support_modules(self, path: str):
        package_len = len(path) - len(os.path.basename(path))
        files = glob.glob(path + '/**/*.py', recursive=True)
        for file in files:
            file_name = os.path.basename(file)
            if self.__TEST_PREFIX not in file_name and '__init__' not in file_name:
                module = file[package_len:].replace('/', '.')[:-3]
                if module in sys.modules:
                    importlib.reload(sys.modules[module])

    def __load_test_class(self, file_name, test_name):
        file = glob.glob(os.path.join(self.__tests_path, file_name + '.py'))
        if len(file) == 0:
            return None
        file = file[0]
        test_container = TestContainer(file)
        module = self.__load_module(file, file)
        members = [o for o in inspect.getmembers(module) if inspect.isclass(o[1])]
        for member in members:
            class_name = member[0]
            class_type = member[1]
            if class_name.lower() == test_name and module.__file__ == class_type.__module__:
                test_class = TestClass(class_name, class_type)
                test_container.add_test_class(test_class)
        return test_container

    def __load_test_classes(self):
        files = glob.glob(self.__tests_path + f'/**/{self.__TEST_PREFIX}*.py', recursive=True)
        all_test_containers = []
        for file in files:
            test_container = TestContainer(file)
            all_test_containers.append(test_container)
            module = self.__load_module(file, file)
            members = [o for o in inspect.getmembers(module) if inspect.isclass(o[1])]
            for member in members:
                class_name = member[0]
                class_type = member[1]
                if module.__file__ == class_type.__module__:
                    test_class = TestClass(class_name, class_type)
                    test_container.add_test_class(test_class)
        return all_test_containers
