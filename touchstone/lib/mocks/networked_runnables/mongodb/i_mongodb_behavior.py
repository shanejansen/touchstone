import abc

from touchstone.lib.mocks.networked_runnables.mongodb.mongodb_setup import MongodbSetup
from touchstone.lib.mocks.networked_runnables.mongodb.mongodb_verify import MongodbVerify


class IMongodbBehavior(object):
    @abc.abstractmethod
    def setup(self) -> MongodbSetup:
        pass

    @abc.abstractmethod
    def verify(self) -> MongodbVerify:
        pass
