from pymongo import MongoClient

from touchstone.lib.mocks.networked_runnables.mongodb.docker.docker_mongo_context import DockerMongoContext
from touchstone.lib.mocks.networked_runnables.mongodb.i_mongodb_behavior import IMongodbVerify


class DockerMongodbVerify(IMongodbVerify):
    def __init__(self, mongo_context: DockerMongoContext):
        self.__mongo_context = mongo_context
        self.__mongo_client = None

    def set_mongo_client(self, mongo_client: MongoClient):
        self.__mongo_client = mongo_client

    def document_exists(self, database: str, collection: str, document: dict, num_expected: int = 1) -> bool:
        if not self.__mongo_context.collection_exists(database, collection):
            return False

        num_documents = self.__mongo_client \
            .get_database(database) \
            .get_collection(collection) \
            .count_documents(document)

        if not num_expected and num_documents != 0:
            return True
        if num_expected == num_documents:
            return True
        print(f'Document: "{document}" in collection: "{collection}" was found {num_documents} time(s) but expected '
              f'{num_expected if num_expected else "any"} time(s).')
        return False
