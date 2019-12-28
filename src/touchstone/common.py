import logging
import os
import sys

import yaml

from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.docker_manager import DockerManager

logger = logging.getLogger('touchstone')


def load_config():
    path = os.path.join(TouchstoneConfig.instance().config['root'], 'touchstone.yml')
    with open(path, 'r') as file:
        TouchstoneConfig.instance().merge(yaml.safe_load(file))


def sanity_check_passes() -> bool:
    touchstone_path = os.path.join(TouchstoneConfig.instance().config['root'], 'touchstone.yml')
    defaults_path = os.path.join(TouchstoneConfig.instance().config['root'], 'defaults')
    return os.path.exists(touchstone_path) and os.path.exists(defaults_path)


def prep_run():
    if not sanity_check_passes():
        print('touchstone.yml and the defaults directory could not be found. '
              'If touchstone has not been initialized, run \'touchstone init\'.')
        exit(1)
    load_config()


def exit_touchstone(is_successful: bool):
    print('Shutting down...')
    if is_successful:
        code = 0
    else:
        code = 1
    DockerManager.instance().cleanup()
    sys.exit(code)
