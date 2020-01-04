from touchstone import common


class TouchstoneConfig:
    def __init__(self, root):
        self.config: dict = {
            'root': root,
            'dev': False,
            'host': 'localhost',
            'mocks': [],
            'services': []
        }

    def set_dev(self):
        self.config['dev'] = True

    def merge(self, other: dict):
        self.config = common.dict_merge(self.config, other)
