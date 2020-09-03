from typing import List, Iterable

from pymysql.cursors import Cursor

from touchstone import common
from touchstone.lib.mocks.networked_runnables.mysql.docker.docker_mysql_context import DockerMysqlContext
from touchstone.lib.mocks.networked_runnables.mysql.i_mysql_behabior import IMysqlSetup


class DockerMysqlSetup(IMysqlSetup):
    def __init__(self, mysql_context: DockerMysqlContext):
        self.__mysql_context = mysql_context
        self.__cursor = None
        self.__convert_camel_to_snake = False

    def set_cursor(self, cursor: Cursor):
        self.__cursor = cursor

    def set_convert_camel_to_snake(self, convert_camel_to_snake: bool):
        self.__convert_camel_to_snake = convert_camel_to_snake

    def recreate_databases(self):
        for database in self.__mysql_context.databases:
            self.__cursor.execute(f'DROP DATABASE {database}')
            self.__cursor.execute(f'CREATE DATABASE {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')

    def init(self, defaults: dict):
        for database in self.__mysql_context.databases:
            self.__cursor.execute(f'DROP DATABASE {database}')
        self.__mysql_context.clear()

        for database in defaults.get('databases', []):
            database_name = database['name']
            self.__cursor.execute(f'CREATE DATABASE {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
            self.__cursor.execute(f'USE {database_name}')
            self.__mysql_context.add_database(database_name)
            for statement in database.get('statements', []):
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
            sql = self.__build_insert_sql(table, data.keys(), values)
            common.logger.debug(f'Executing: {sql}')
            self.__cursor.execute(f'USE {database}')
            self.__cursor.execute(sql, data)

    def insert_rows(self, database: str, table: str, data: List[dict]):
        for datum in data:
            self.insert_row(database, table, datum)

    def __sql_values_from_dict(self, data: dict) -> str:
        col_values = []
        for key, value in data.items():
            if value is None:
                col_values.append('NULL')
            else:
                col_values.append(f'%({key})s')
        col_values = ', '.join(col_values)
        return '(' + col_values + ')'

    def __sql_values_from_list(self, data: List[dict]) -> str:
        values = []
        for datum in data:
            values.append(self.__sql_values_from_dict(datum))
        return ', '.join(values)

    def __build_insert_sql(self, table: str, cols: Iterable, values: str) -> str:
        col_names = ', '.join(cols)
        return f"INSERT INTO {table} ({col_names}) VALUES {values}"
