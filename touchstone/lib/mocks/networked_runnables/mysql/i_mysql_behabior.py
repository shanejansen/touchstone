import abc
from typing import List


class IMysqlSetup(object):
    @abc.abstractmethod
    def execute(self, database: str, sql: str):
        pass

    @abc.abstractmethod
    def insert_row(self, database: str, table: str, data: dict):
        pass

    @abc.abstractmethod
    def insert_rows(self, database: str, table: str, data: List[dict]):
        pass


class IMysqlVerify(object):
    @abc.abstractmethod
    def row_exists(self, database: str, table: str, where_conditions: dict, num_expected: int = 1) -> bool:
        """Returns True if the given where conditions are found in the given database. If num_expected is set to None,
        any number of rows will be considered passing."""
        pass

    @abc.abstractmethod
    def row_does_not_exist(self, database: str, table: str, where_conditions: dict) -> bool:
        """Returns True if the given where conditions are not found in the given database."""
        pass


class IMysqlBehavior(object):
    DEFAULT_CONFIG = {
        'convertCamelToSnakeCase': True
    }

    @abc.abstractmethod
    def setup(self) -> IMysqlSetup:
        pass

    @abc.abstractmethod
    def verify(self) -> IMysqlVerify:
        pass
