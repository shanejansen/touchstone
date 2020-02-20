import glob
import importlib.util
import os
import sys
import time

package_dir = '/Users/s560879/Documents/GitRepos/tindr-service/touchstone/tests'


def load_package():
    pkg_spec = importlib.util.spec_from_file_location(os.path.basename(package_dir), package_dir + '/__init__.py')
    pkg_module = importlib.util.module_from_spec(pkg_spec)
    sys.modules[pkg_spec.name] = pkg_module
    pkg_spec.loader.exec_module(pkg_module)


def load_test():
    spec = importlib.util.spec_from_file_location(package_dir + '/test_data_emit.py',
                                                  package_dir + '/test_data_emit.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)


def reload_support_modules():
    package_len = len(package_dir) - len(os.path.basename(package_dir))
    files = glob.glob(package_dir + '/**/*.py', recursive=True)
    for file in files:
        file_name = os.path.basename(file)
        if 'test_' not in file_name and '__init__' not in file_name:
            module = file[package_len:].replace('/', '.')[:-3]
            if module in sys.modules:
                importlib.reload(sys.modules[module])


load_package()
reload_support_modules()
load_test()

time.sleep(5)

load_package()
reload_support_modules()
load_test()
