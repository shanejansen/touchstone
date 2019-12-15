import json
import os

import sys

from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.docker_manager import DockerManager


def load_config():
    path = os.path.join(TouchstoneConfig.instance().config['root'], 'touchstone.json')
    with open(path, 'r') as file:
        TouchstoneConfig.instance().merge(json.load(file))


def sanity_check_passes() -> bool:
    touchstone_json_path = os.path.join(TouchstoneConfig.instance().config['root'], 'touchstone.json')
    defaults_path = os.path.join(TouchstoneConfig.instance().config['root'], 'defaults')
    return os.path.exists(touchstone_json_path) and os.path.exists(defaults_path)


def prep_run():
    if not sanity_check_passes():
        print('touchstone.json and the defaults directory could not be found. '
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
