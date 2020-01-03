import sys

from touchstone.lib import common


class TouchstoneConfig:
    __instance: 'TouchstoneConfig' = None

    @staticmethod
    def instance() -> 'TouchstoneConfig':
        if TouchstoneConfig.__instance is None:
            TouchstoneConfig()
        return TouchstoneConfig.__instance

    def __init__(self):
        TouchstoneConfig.__instance = self
        self.config: dict = {
            'root': None,
            'dev': False,
            'host': 'localhost',
            'mocks': [],
            'services': []
        }

        if 'dev' in sys.argv:
            self.config['dev'] = True

    def set_root(self, root: str):
        self.config['root'] = root

    def set_dev(self):
        self.config['dev'] = True

    def merge(self, other: dict):
        self.config = common.dict_merge(self.config, other)
