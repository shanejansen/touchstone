import glob
import os
import sys
from pathlib import Path

import yaml

from touchstone.lib import exceptions
from touchstone.lib.configurers.service_config import ServiceConfig
from touchstone.lib.configurers.touchstone_config import TouchstoneConfig
from touchstone.lib.managers.docker_manager import DockerManager
from touchstone.lib.nodes.deps.dep_factory import DepFactory
from touchstone.lib.nodes.deps.deps import Deps
from touchstone.lib.nodes.services.service_factory import ServiceFactory
from touchstone.lib.nodes.services.services import Services
from touchstone.lib.tests import Tests
from touchstone.lib.ts_context import TsContext


class Bootstrap(object):
    def __init__(self, is_dev_mode=False, should_log_services=False):
        root = os.path.join(os.getcwd(), 'touchstone')
        touchstone_config = self.__build_touchstone_config(root)
        log_directory = None
        if should_log_services:
            log_directory = os.path.join(root, 'logs')
            os.makedirs(log_directory, exist_ok=True)
        self.ts_context = TsContext()
        self.docker_manager = DockerManager(should_auto_discover=not is_dev_mode)
        self.deps = self.__build_deps(is_dev_mode,
                                      touchstone_config.get_config()['root'],
                                      touchstone_config.get_config()['dependencies'])
        self.services = self.__build_services(is_dev_mode,
                                              touchstone_config.get_config()['root'],
                                              touchstone_config.get_config()['services'],
                                              self.deps, log_directory)

    def __build_touchstone_config(self, root) -> TouchstoneConfig:
        config = TouchstoneConfig(root)
        path = os.path.join(root, 'touchstone.yml')
        with open(path, 'r') as file:
            config.merge_config(yaml.safe_load(file))
        config.verify()
        return config

    def __build_deps(self, is_dev_mode, root, configs) -> Deps:
        defaults_paths = {}
        default_files = glob.glob(os.path.join(root, 'defaults') + '/*.yml')
        for default_file in default_files:
            defaults_paths[Path(default_file).stem] = default_file

        deps = Deps()
        dep_factory = DepFactory(self.ts_context, is_dev_mode, root, defaults_paths, configs, self.docker_manager)
        for dep_name in configs:
            dep = dep_factory.get_dep(dep_name)
            if not dep:
                raise exceptions.DepNotSupportedException(f'Dependency: {dep_name} is not supported.')
            setattr(deps, dep_name, dep.get_behavior())
            deps.register_dep(dep)
        return deps

    def __build_services(self, is_dev_mode, root, user_service_configs, deps, log_directory) -> Services:
        services = Services()
        service_factory = ServiceFactory(is_dev_mode, root, self.docker_manager, log_directory)
        for user_service_config in user_service_configs:
            service_config = ServiceConfig()
            service_config.merge_config(user_service_config)
            service_config.verify()
            if service_config.get_config()['tests'] is None:
                tests = None
            else:
                tests_path = os.path.abspath(os.path.join(root, service_config.get_config()['tests']))
                tests = Tests(deps, services, tests_path)
            service = service_factory.get_service(service_config, tests)
            services.add_service(service)
        return services

    def cleanup(self):
        self.services.stop()
        self.deps.stop()
        self.docker_manager.cleanup()

    def exit(self, is_successful: bool):
        print('Shutting down...')
        if is_successful:
            code = 0
        else:
            code = 1
        self.cleanup()
        sys.exit(code)
