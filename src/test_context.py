from configs.service_config import Config
from mocks.mocks import Mocks


class TestContext(object):
    def __init__(self, config: Config, mocks: Mocks):
        self.config = config
        self.mocks = mocks
