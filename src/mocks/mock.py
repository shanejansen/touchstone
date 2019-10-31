import abc


class Mock(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, mock_config):
        self.mock_config = mock_config

    @staticmethod
    def name():
        """The name of this mock. This is used to match the mock type in touchstone.json"""

    @staticmethod
    def pretty_name():
        """A pretty, display name for this mock"""
        return "Undefined"

    @abc.abstractmethod
    def default_exposed_port(self):
        """The default port where this mock will be exposed. Be sure to call the method exposed_port() in case it
        has been overridden"""
        return None

    @abc.abstractmethod
    def start(self, dev_mode=False):
        """Starts this mock"""

    def exposed_port(self):
        if 'port' in self.mock_config:
            return self.mock_config['port']
        return self.default_exposed_port()