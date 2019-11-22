import sys


class TouchstoneConfig:
    __instance = None

    @staticmethod
    def instance():
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
        self.config = dict(list(self.config.items()) + list(other.items()))
