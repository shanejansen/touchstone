from pymysql.cursors import Cursor

from touchstone.lib.mocks.mysql.mysql_context import MysqlContext


class MysqlVerify(object):
    def __init__(self, cursor: Cursor, mysql_context: MysqlContext):
        self.__cursor = cursor
        self.__mysql_context = mysql_context

    # def fetch_one(self, database: str, sql: str) -> dict:
    #     self.__cursor.execute(f'USE {database}')
    #     self.__cursor.execute(sql)
    #     return self.__cursor.fetchone()
    #
    # def fetch_many(self, database: str, sql: str) -> List[dict]:
    #     self.__cursor.execute(f'USE {database}')
    #     self.__cursor.execute(sql)
    #     return self.__cursor.fetchmany()
