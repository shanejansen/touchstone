import abc

from touchstone.lib.mocks.networked_runnables.rabbitmq.rabbitmq_setup import RabbitmqSetup
from touchstone.lib.mocks.networked_runnables.rabbitmq.rabbitmq_verify import RabbitmqVerify


class IRabbitmqBehavior(object):
    @abc.abstractmethod
    def setup(self) -> RabbitmqSetup:
        pass

    @abc.abstractmethod
    def verify(self) -> RabbitmqVerify:
        pass
