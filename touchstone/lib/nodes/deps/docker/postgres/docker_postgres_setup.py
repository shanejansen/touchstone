from typing import List, Iterable

import psycopg2

from touchstone import common
from touchstone.lib.nodes.deps.behaviors.i_database_behabior import IDatabaseSetup
from touchstone.lib.nodes.deps.docker.postgres.docker_postgres_context import DockerPostgresContext


class DockerPostgresSetup(IDatabaseSetup):
    def __init__(self, postgres_context: DockerPostgresContext):
        self.__postgres_context = postgres_context
        self.__cursor = None
        self.__convert_camel_to_snake = False

    def set_cursor(self, cursor):
        self.__cursor = cursor

    def set_convert_camel_to_snake(self, convert_camel_to_snake: bool):
        self.__convert_camel_to_snake = convert_camel_to_snake

    def recreate_databases(self):
        for database in self.__postgres_context.databases:
            self.__cursor.execute(f'DROP SCHEMA {database}')
            self.__cursor.execute(f'CREATE SCHEMA {database}')

    def init(self, defaults: dict):
        for database in self.__postgres_context.databases:
            self.__cursor.execute(f'DROP SCHEMA {database} CASCADE')
        self.__postgres_context.clear()

        for database in defaults.get('databases', []):
            database_name = database['name']
            try:
                self.__cursor.execute(f'CREATE SCHEMA {database_name}')
            except psycopg2.errors.DuplicateSchema:
                pass
            self.__cursor.execute(f'SET search_path TO {database_name}')
            self.__postgres_context.add_database(database_name)
            for statement in database.get('statements', []):
                self.__cursor.execute(statement)

    def execute(self, database: str, sql: str):
        if self.__postgres_context.database_exists(database):
            self.__cursor.execute(f'SET search_path TO {database}')
            self.__cursor.execute(sql)

    def insert_row(self, database: str, table: str, data: dict):
        if self.__postgres_context.database_exists(database):
            if self.__convert_camel_to_snake:
                data = common.to_snake(data)
            values = self.__sql_values_from_dict(data)
            sql = self.__build_insert_sql(table, data.keys(), values)
            common.logger.debug(f'Executing: {sql}')
            self.__cursor.execute(f'SET search_path TO {database}')
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
