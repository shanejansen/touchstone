from pymysql.cursors import Cursor

from touchstone.lib.mocks.mysql.mysql_context import MysqlContext


class MysqlSetup(object):
    def __init__(self, cursor: Cursor, mysql_context: MysqlContext):
        self.__cursor = cursor
        self.__mysql_context = mysql_context

    def load_defaults(self, defaults: dict):
        for database in self.__mysql_context.databases:
            self.__cursor.execute(f'DROP DATABASE {database}')
        self.__mysql_context.clear()

        for database in defaults['databases']:
            database_name = database['name']
            self.__cursor.execute(f'CREATE DATABASE {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
            self.__cursor.execute(f'USE {database_name}')
            self.__mysql_context.add_database(database_name)
            for statement in database['statements']:
                self.__cursor.execute(statement)

    def execute(self, database: str, sql: str):
        if self.__mysql_context.database_exists(database):
            self.__cursor.execute(f'USE {database}')
            self.__cursor.execute(sql)
