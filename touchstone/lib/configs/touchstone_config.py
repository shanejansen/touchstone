from touchstone import common


class TouchstoneConfig:
    def __init__(self, root):
        self.config: dict = {
            'root': root,
            'services': [],
            'mocks': []
        }

    def merge(self, other: dict):
        self.config = common.dict_merge(self.config, other)
        if not self.config['services']:
            self.config['services'] = []
        if not self.config['mocks']:
            self.config['mocks'] = []
