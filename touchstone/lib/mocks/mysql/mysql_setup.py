from typing import List

from pymysql.cursors import Cursor

from touchstone import common
from touchstone.lib.mocks.mysql.mysql_context import MysqlContext


class MysqlSetup(object):
    def __init__(self, cursor: Cursor, mysql_context: MysqlContext, convert_camel_to_snake: bool):
        self.__cursor = cursor
        self.__mysql_context = mysql_context
        self.__convert_camel_to_snake = convert_camel_to_snake

    def init(self, defaults: dict):
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
            if self.__convert_camel_to_snake:
                data = common.to_snake(data)
            values = self.__sql_values_from_dict(data)
            sql = self.__build_insert_sql(table, data, values)
            common.logger.debug(f'Executing: {sql}')
            self.__cursor.execute(f'USE {database}')
            self.__cursor.execute(sql)

    def insert_rows(self, database: str, table: str, data: List[dict]):
        if self.__mysql_context.database_exists(database):
            if self.__convert_camel_to_snake:
                data = common.to_snake(data)
            values = self.__sql_values_from_list(data)
            sql = self.__build_insert_sql(table, data[0], values)
            common.logger.debug(f'Executing: {sql}')
            self.__cursor.execute(f'USE {database}')
            self.__cursor.execute(sql)

    def __sql_values_from_dict(self, data: dict) -> str:
        col_values = []
        for value in data.values():
            col_values.append(f"'{value}'")
        col_values = ', '.join(col_values)
        return '(' + col_values + ')'

    def __sql_values_from_list(self, data: List[dict]) -> str:
        values = []
        for datum in data:
            values.append(self.__sql_values_from_dict(datum))
        return ', '.join(values)

    def __build_insert_sql(self, table: str, cols: dict, values: str) -> str:
        col_names = ', '.join(cols.keys())
        return f"INSERT INTO {table} ({col_names}) VALUES {values}"
