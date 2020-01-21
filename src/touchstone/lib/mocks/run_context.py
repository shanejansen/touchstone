from touchstone.lib.mocks.network import Network


class RunContext(object):
    def __init__(self, name: str, network: Network):
        self.name = name
        self.network = network
