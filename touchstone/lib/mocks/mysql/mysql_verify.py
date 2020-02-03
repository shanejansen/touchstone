from pymysql.cursors import Cursor

from touchstone import common
from touchstone.lib.mocks.mysql.mysql_context import MysqlContext


class MysqlVerify(object):
    def __init__(self, cursor: Cursor, mysql_context: MysqlContext, convert_camel_to_snake: bool):
        self.__cursor = cursor
        self.__mysql_context = mysql_context
        self.__convert_camel_to_snake = convert_camel_to_snake

    def row_exists(self, database: str, table: str, where_conditions: dict, num_expected: int = 1) -> bool:
        """Returns True if the given where conditions are found in the given database. If num_expected is set to None,
        any number of rows will be considered passing."""
        if not self.__mysql_context.database_exists(database):
            return False

        if self.__convert_camel_to_snake:
            where_conditions = common.to_snake(where_conditions)
        where = []
        for key, value in where_conditions.items():
            where.append(f"{key}='{value}'")
        sql = f"SELECT COUNT(*) FROM {table} WHERE {' AND '.join(where)}"
        common.logger.debug(f'Executing: {sql}')
        self.__cursor.execute(f'USE {database}')
        self.__cursor.execute(sql)
        num_rows = self.__cursor.fetchone()['COUNT(*)']

        if not num_expected and num_rows != 0:
            return True
        if num_expected == num_rows:
            return True
        print(f'SQL: "{sql}" in database: "{database}" was found {num_rows} time(s) but expected '
              f'{num_expected if num_expected else "any"} time(s).')
        return False

    def row_does_not_exist(self, database: str, table: str, where_conditions: dict) -> bool:
        """Returns True if the given where conditions are not found in the given database."""
        return self.row_exists(database, table, where_conditions, num_expected=0)
