import abc

from touchstone.lib.mocks.networked_runnables.mysql.mysql_setup import MysqlSetup
from touchstone.lib.mocks.networked_runnables.mysql.mysql_verify import MysqlVerify


class IMysqlBehavior(object):
    @abc.abstractmethod
    def setup(self) -> MysqlSetup:
        pass

    @abc.abstractmethod
    def verify(self) -> MysqlVerify:
        pass
