from typing import List

from pymongo import MongoClient

from touchstone.lib.mocks.mongodb.mongo_context import MongoContext


class MongodbSetup(object):
    def __init__(self, mongo_client: MongoClient, mongo_context: MongoContext):
        self.__mongo_client = mongo_client
        self.__mongo_context = mongo_context

    def init(self, defaults: dict):
        for database in self.__mongo_context.databases():
            mongo_database = self.__mongo_client.get_database(database)
            for collection in self.__mongo_context.collections(database):
                mongo_database.drop_collection(collection)
        self.__mongo_context.clear()

        for database in defaults['databases']:
            database_name = database['name']
            mongo_database = self.__mongo_client.get_database(database_name)
            self.__mongo_context.add_database(database_name)
            if 'collections' in database:
                for collection in database['collections']:
                    mongo_collection = mongo_database.get_collection(collection['name'])
                    self.__mongo_context.add_collection(database_name, collection['name'])
                    if 'documents' in collection:
                        for document in collection['documents']:
                            mongo_collection.insert_one(document)

    def command(self, database: str, command: dict):
        """Execute an arbitrary command on the database."""
        if self.__mongo_context.database_exists(database):
            self.__mongo_client.get_database(database).command(command)

    def insert_document(self, database: str, collection: str, document: dict):
        if self.__mongo_context.collection_exists(database, collection):
            self.__mongo_client \
                .get_database(database) \
                .get_collection(collection).insert_one(document)

    def insert_documents(self, database: str, collection: str, documents: List[dict]):
        if self.__mongo_context.collection_exists(database, collection):
            self.__mongo_client \
                .get_database(database) \
                .get_collection(collection).insert_many(documents)
