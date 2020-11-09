import logging
import os
import re
from typing import List

import yaml

from touchstone import __version__
from touchstone.lib import exceptions

logger = logging.getLogger('touchstone')
__camel_to_snake_pattern = re.compile(r'(?<!^)(?=[A-Z])')


def sanity_check_passes() -> bool:
    # Ensure paths and files exist
    touchstone_path = os.path.join(os.getcwd(), 'touchstone')
    touchstone_yml_path = os.path.join(touchstone_path, 'touchstone.yml')
    defaults_path = os.path.join(touchstone_path, 'defaults')
    paths_exist = os.path.exists(touchstone_path) \
                  and os.path.exists(touchstone_yml_path) \
                  and os.path.exists(defaults_path)
    if not paths_exist:
        print('The touchstone directory, touchstone.yml, or the defaults directory could not be found. '
              'If touchstone has not been initialized, run \'touchstone init\'.')
        return False

    # Ensure versions are compatible
    versions_match = False
    with open(touchstone_yml_path, 'r') as file:
        touchstone_config = yaml.safe_load(file)
        given_version = touchstone_config.get('touchstone_version')
        if given_version:
            split_given_version = str.split(given_version, '.')
            split_current_version = str.split(__version__, '.')
            versions_match = split_given_version[0] == split_current_version[0] \
                             and split_given_version[1] <= split_current_version[1]
            if not versions_match:
                print(f'Version defined in touchstone.yml: "{given_version}" is not compatible with system Touchstone '
                      f'version:"{__version__}"')
        else:
            print('A touchstone version number must be defined in "touchstone.yml".')
    return versions_match


def dict_merge(base: dict, override: dict) -> dict:
    if override is None:
        return base
    return dict(list(base.items()) + list(override.items()))


def __camel_to_snake(input: str) -> str:
    return __camel_to_snake_pattern.sub('_', input).lower()


def __dict_keys_to_snake(input: dict) -> dict:
    new = {}
    for key, value in input.items():
        new[__camel_to_snake(key)] = value
    return new


def __list_dict_keys_to_snake(input: List[dict]) -> List[dict]:
    new = []
    for item in input:
        new.append(__dict_keys_to_snake(item))
    return new


def to_snake(input) -> object:
    if isinstance(input, str):
        return __camel_to_snake(input)
    if isinstance(input, dict):
        return __dict_keys_to_snake(input)
    if isinstance(input, list):
        return __list_dict_keys_to_snake(input)
    raise exceptions.TouchstoneException('Given input can not be converted to snake case.')
