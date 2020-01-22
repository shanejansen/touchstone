from pymysql.cursors import Cursor

from touchstone import common
from touchstone.lib.mocks.mysql.mysql_context import MysqlContext


class MysqlVerify(object):
    def __init__(self, cursor: Cursor, mysql_context: MysqlContext):
        self.__cursor = cursor
        self.__mysql_context = mysql_context

    def row_exists(self, database: str, table: str, where_conditions: dict, num_expected: int = 1) -> bool:
        """Returns True if the executed sql if found in the given database. If num_expected is set to None, any number
        of rows will be considered passing."""
        if not self.__mysql_context.database_exists(database):
            return False

        where = []
        for key, value in where_conditions.items():
            where.append(f"{key}='{value}'")
        sql = f"SELECT COUNT(*) FROM {table} WHERE {' AND '.join(where)}"
        common.logger.debug(f'Executing: {sql}')
        self.__cursor.execute(f'USE {database}')
        self.__cursor.execute(sql)
        num_rows = self.__cursor.rowcount

        if not num_expected and num_rows != 0:
            return True
        if num_expected == num_rows:
            return True
        print(f'Executed SQL: "{sql}" in database: "{database}" was found {num_rows} time(s) but expected '
              f'{num_expected if num_expected else "any"} time(s).')
        return False
