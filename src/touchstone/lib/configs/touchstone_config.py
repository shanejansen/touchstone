from touchstone import common


class TouchstoneConfig:
    def __init__(self, root):
        self.config: dict = {
            'root': root,
            'host': 'localhost',
            'services': [],
            'mocks': []
        }

    def merge(self, other: dict):
        self.config = common.dict_merge(self.config, other)
