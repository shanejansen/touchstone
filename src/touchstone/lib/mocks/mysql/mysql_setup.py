from typing import List

from pymysql.cursors import Cursor

from touchstone import common
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

    def insert_row(self, database: str, table: str, data: dict):
        if self.__mysql_context.database_exists(database):
            sql = self.__build_insert_sql_from_dict(table, data)
            common.logger.debug(f'Executing: {sql}')
            self.__cursor.execute(f'USE {database}')
            self.__cursor.execute(sql)

    def insert_rows(self, database: str, table: str, data: List[dict]):
        sql = ''
        if self.__mysql_context.database_exists(database):
            for datum in data:
                sql += self.__build_insert_sql_from_dict(table, datum) + '; '
        common.logger.debug(f'Executing: {sql}')
        self.__cursor.execute(f'USE {database}')
        self.__cursor.execute(sql)
        # INSERT INTO tbl_name
        #     (a,b,c)
        # VALUES
        # (1,2,3),
        # (4,5,6),
        # (7,8,9);

    def __build_insert_sql_from_dict(self, table: str, data: dict) -> str:
        col_names = ', '.join(data.keys())
        col_values = []
        for value in data.values():
            col_values.append(f"'{value}'")
        return f"INSERT INTO {table} ({col_names}) VALUES ({', '.join(col_values)})"
