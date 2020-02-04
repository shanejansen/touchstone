import logging
import os
import re
from typing import List

from touchstone.lib import exceptions

logger = logging.getLogger('touchstone')
__camel_to_snake_pattern = re.compile(r'(?<!^)(?=[A-Z])')


def sanity_check_passes() -> bool:
    touchstone_path = os.path.join(os.getcwd(), 'touchstone.yml')
    defaults_path = os.path.join(os.getcwd(), 'defaults')
    return os.path.exists(touchstone_path) and os.path.exists(defaults_path)


def prep_run():
    if not sanity_check_passes():
        print('touchstone.yml and the defaults directory could not be found. '
              'If touchstone has not been initialized, run \'touchstone init\'.')
        exit(1)


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
