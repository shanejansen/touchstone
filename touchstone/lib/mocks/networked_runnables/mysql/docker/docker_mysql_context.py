class DockerMysqlContext(object):
    def __init__(self):
        self.__databases = []

    @property
    def databases(self) -> list:
        return self.__databases.copy()

    def add_database(self, database: str):
        self.__databases.append(database)

    def database_exists(self, database: str, print_warning=True) -> bool:
        if database in self.__databases:
            return True
        if print_warning:
            print(f'This database: "{database}" is not defined. Check your "mysql.yml" defaults.')
        return False

    def clear(self):
        self.__databases = []
