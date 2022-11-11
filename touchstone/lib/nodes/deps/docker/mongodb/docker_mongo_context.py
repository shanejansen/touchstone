from typing import KeysView


class DockerMongoContext(object):
    def __init__(self):
        self.__databases = {}

    def databases(self) -> KeysView:
        return self.__databases.keys()

    def collections(self, database: str) -> list:
        return self.__databases[database]

    def add_database(self, database: str):
        self.__databases[database] = []

    def add_collection(self, database: str, collection: str):
        self.__databases[database].append(collection)

    def database_exists(self, database: str, print_warning=True) -> bool:
        if database in self.__databases:
            return True
        if print_warning:
            print(f'This database: "{database}" is not defined. Check your "mongodb.yml" defaults.')
        return False

    def collection_exists(self, database: str, collection: str, print_warning=True) -> bool:
        if database in self.__databases and collection in self.__databases[database]:
            return True
        if print_warning:
            print(f'This database: "{database}", collection: "{collection}" is not defined. Check your "mongodb.yml" '
                  f'defaults.')
        return False

    def clear(self):
        self.__databases = {}
