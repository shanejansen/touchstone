import abc


class Setup(object):
    def __init__(self, exposed_port: int):
        self.exposed_port: int = exposed_port

    @abc.abstractmethod
    def load_defaults(self, defaults: dict):
        """Load defaults for this mock provided by the user for dev purposes"""

    @abc.abstractmethod
    def cleanup(self):
        """Cleanup this mock to prepare for the next test"""


class Exercise(object):
    def __init__(self, exposed_port: int):
        self.exposed_port: int = exposed_port


class Verify(object):
    def __init__(self, exposed_port: int):
        self.exposed_port: int = exposed_port
