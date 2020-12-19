from touchstone import common
from touchstone.lib import exceptions


class TouchstoneConfig:
    def __init__(self, root):
        self.config: dict = {
            'root': root,
            'services': [],
            'mocks': []
        }

    def merge(self, other: dict):
        self.config = common.dict_merge(self.config, other)

    def verify(self):
        if self.config['services'] is None:
            raise exceptions.TouchstoneException(f'"services" has not been set. Check your "touchstone.yml".')
        if self.config['mocks'] is None:
            raise exceptions.TouchstoneException(f'"mocks" has not been set. Check your "touchstone.yml".')
