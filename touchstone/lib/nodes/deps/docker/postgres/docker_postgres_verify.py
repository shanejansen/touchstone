from touchstone import common
from touchstone.helpers import validation

from touchstone.lib.nodes.deps.behaviors.i_database_behabior import IDatabaseVerify
from touchstone.lib.nodes.deps.docker.postgres.docker_postgres_context import DockerPostgresContext


class DockerPostgresVerify(IDatabaseVerify):
    def __init__(self, postgres_context: DockerPostgresContext):
        self.__postgres_context = postgres_context
        self.__cursor = None
        self.__convert_camel_to_snake = False

    def set_cursor(self, cursor):
        self.__cursor = cursor

    def set_convert_camel_to_snake(self, convert_camel_to_snake: bool):
        self.__convert_camel_to_snake = convert_camel_to_snake

    def row_exists(self, database: str, table: str, where_conditions: dict, num_expected: int = 1) -> bool:
        if not self.__postgres_context.database_exists(database):
            return False

        if self.__convert_camel_to_snake:
            where_conditions = common.to_snake(where_conditions)
        where = []
        user_values = {}
        for key, value in where_conditions.items():
            if value is None:
                where.append(f'{key} IS NULL')
            elif value is validation.ANY:
                where.append(f'{key} IS NOT NULL')
            else:
                where.append(f'{key}=%({key})s')
                user_values[key] = value
        sql = f"SELECT COUNT(*) FROM {table} WHERE {' AND '.join(where)}"
        common.logger.debug(f'Executing: {sql}')
        self.__cursor.execute(f'SET search_path TO {database}')
        self.__cursor.execute(sql, user_values)
        num_rows = self.__cursor.fetchone()[0]

        if num_expected is None and num_rows != 0:
            return True
        if num_expected == num_rows:
            return True
        print(f'SQL: "{sql}" in schema: "{database}" was found {num_rows} time(s) but expected '
              f'{num_expected if num_expected else "any"} time(s).')
        return False

    def row_does_not_exist(self, database: str, table: str, where_conditions: dict) -> bool:
        return self.row_exists(database, table, where_conditions, num_expected=0)
