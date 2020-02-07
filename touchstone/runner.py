import sys

from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.docker_manager import DockerManager


class Runner(object):
    def __init__(self, touchstone_config: TouchstoneConfig, docker_manager: DockerManager):
        self.__touchstone_config = touchstone_config
        self.__docker_manager = docker_manager

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
