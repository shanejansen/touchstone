import glob
import importlib.util
import inspect

from touchstone.lib.mocks.mocks import Mocks


class Tests(object):
    def __init__(self, mocks: Mocks, tests_path: str):
        self.mocks = mocks
        self.tests_path = tests_path

    def run(self) -> bool:
        class_defs = self.__load_test_classes()

        tests_passed = True
        for class_def in class_defs:
            name = class_def['name']
            clazz = class_def['class']
            print(f'{name} :: RUNNING')
            clazz.given()
            result = clazz.when()
            did_pass = clazz.then(result)
            if not did_pass:
                print(f'{name} :: FAILED. Unexpected value "{result}"\n')
                tests_passed = False
            else:
                print(f'{name} :: PASSED\n')
            self.mocks.cleanup()
        return tests_passed

    def __load_test_classes(self):
        files = glob.glob(f'{self.tests_path}/*.py')
        class_defs = []
        for file in files:
            spec = importlib.util.spec_from_file_location(file, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            members = [o for o in inspect.getmembers(module) if inspect.isclass(o[1])]
            for member in members:
                class_name = member[0]
                class_type = member[1]
                if module.__file__ == class_type.__module__:
                    clazz = class_type(self.mocks)
                    class_def = {
                        'name': class_name,
                        'class': clazz
                    }
                    class_defs.append(class_def)
        return class_defs
