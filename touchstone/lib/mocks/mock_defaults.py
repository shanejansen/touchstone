import os

import yaml


class MockDefaults(object):
    def __init__(self, path: str):
        self.__path = path

    def get(self, mock_name: str) -> dict:
        try:
            with open(os.path.join(self.__path, f'{mock_name}.yml'), 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            return {}
