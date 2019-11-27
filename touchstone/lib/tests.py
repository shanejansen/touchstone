import glob
import importlib.util
import inspect
import traceback

from touchstone.lib.mocks.mocks import Mocks


class Tests(object):
    def __init__(self, mocks: Mocks, tests_path: str):
        self.mocks = mocks
        self.tests_path = tests_path

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
        all_test_containers = self.__load_test_classes()
        if len(all_test_containers) == 0:
            print(f'No tests found at {self.tests_path}')
            return False

        tests_passed = True
        for test_container in all_test_containers:
            print(test_container.file)
            for test_class in test_container.test_classes:
                class_instance = test_class.clazz(self.mocks)
                print(f'{test_class.name} :: RUNNING')

                did_pass = False
                result = None
                try:
                    class_instance.given()
                    result = class_instance.when()
                    did_pass = class_instance.then(result)
                except Exception as e:
                    traceback.print_tb(e.__traceback__)
                    tests_passed = False

                if not did_pass:
                    print(f'{test_class.name} :: FAILED. Actual result: "{result}"\n')
                    tests_passed = False
                else:
                    print(f'{test_class.name} :: PASSED\n')
                self.mocks.cleanup()
        return tests_passed

    def __load_test_classes(self):
        files = glob.glob(f'{self.tests_path}/*.py')
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
