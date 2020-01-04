import os
import sys

from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.docker_manager import DockerManager


class Runner(object):
    def __init__(self, touchstone_config: TouchstoneConfig, docker_manager: DockerManager):
        self.__touchstone_config = touchstone_config
        self.__docker_manager = docker_manager

    def sanity_check_passes(self) -> bool:
        touchstone_path = os.path.join(self.__touchstone_config.config['root'], 'touchstone.yml')
        defaults_path = os.path.join(self.__touchstone_config.config['root'], 'defaults')
        return os.path.exists(touchstone_path) and os.path.exists(defaults_path)

    def prep_run(self):
        if not self.sanity_check_passes():
            print('touchstone.yml and the defaults directory could not be found. '
                  'If touchstone has not been initialized, run \'touchstone init\'.')
            exit(1)

    def exit_touchstone(self, is_successful: bool):
        print('Shutting down...')
        if is_successful:
            code = 0
        else:
            code = 1
        self.cleanup()
        sys.exit(code)

    def cleanup(self):
        self.__docker_manager.cleanup()
