import abc
from typing import List


class IMysqlSetup(object):
    @abc.abstractmethod
    def execute(self, database: str, sql: str):
        """Executes arbitrary SQL on the given database."""
        pass

    @abc.abstractmethod
    def insert_row(self, database: str, table: str, data: dict):
        """Inserts a dictionary of key-value pairs into the given database and table. If the config option,
        "camel_to_snake" is set (default True), the dictionary keys will be converted from camel case to
        snake case."""
        pass

    @abc.abstractmethod
    def insert_rows(self, database: str, table: str, data: List[dict]):
        """Inserts a list of dictionaries of key-value pairs into the given database and table. If the config option,
        "camel_to_snake" is set (default True), the dictionary keys will be converted from camel case to
        snake case."""
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
        'camel_to_snake': True,
        'snapshot_databases': False
    }

    @abc.abstractmethod
    def setup(self) -> IMysqlSetup:
        pass

    @abc.abstractmethod
    def verify(self) -> IMysqlVerify:
        pass
