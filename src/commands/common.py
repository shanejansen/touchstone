import json
import os
import sys

from configs.touchstone_config import TouchstoneConfig
from docker_manager import DockerManager


def load_config():
    path = os.path.join(TouchstoneConfig.instance().config['root'], 'touchstone.json')
    with open(path, 'r') as file:
        TouchstoneConfig.instance().merge(json.load(file))


def sanity_check_passes() -> bool:
    touchstone_json_path = os.path.join(TouchstoneConfig.instance().config['root'], 'touchstone.json')
    dev_defaults_path = os.path.join(TouchstoneConfig.instance().config['root'], 'dev-defaults')
    return os.path.exists(touchstone_json_path) and os.path.exists(dev_defaults_path)


def exit_touchstone(is_successful: bool):
    print('Exiting...')
    if is_successful:
        code = 0
    else:
        code = 1
    DockerManager.instance().cleanup()
    sys.exit(code)
