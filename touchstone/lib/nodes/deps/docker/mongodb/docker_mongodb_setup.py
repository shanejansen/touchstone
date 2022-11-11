import json
from typing import List

from pymongo import MongoClient

from touchstone.lib.nodes.deps.behaviors.i_mongodb_behavior import IMongodbSetup
from touchstone.lib.nodes.deps.docker.mongodb.docker_mongo_context import DockerMongoContext


class DockerMongodbSetup(IMongodbSetup):
    def __init__(self, mongo_context: DockerMongoContext):
        self.__mongo_context = mongo_context
        self.__mongo_client = None

    def set_mongo_client(self, mongo_client: MongoClient):
        self.__mongo_client = mongo_client

    def init(self, defaults: dict):
        for database in self.__mongo_context.databases():
            mongo_database = self.__mongo_client.get_database(database)
            collections = mongo_database.list_collection_names(filter={"name": {"$regex": r"^(?!system\\.)"}})
            for collection in collections:
                mongo_database.drop_collection(collection)
        self.__mongo_context.clear()

        for database in defaults.get('databases', []):
            database_name = database['name']
            mongo_database = self.__mongo_client.get_database(database_name)
            self.__mongo_context.add_database(database_name)
            for collection in database.get('collections', []):
                mongo_collection = mongo_database.get_collection(collection['name'])
                self.__mongo_context.add_collection(database_name, collection['name'])
                for document in collection.get('documents', []):
                    # Supports multi-line documents
                    if isinstance(document, str):
                        document = json.loads(document)
                    mongo_collection.insert_one(document)

    def command(self, database: str, command: dict):
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
