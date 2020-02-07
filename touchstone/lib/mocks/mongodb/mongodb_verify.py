from pymongo import MongoClient

from touchstone.lib.mocks.mongodb.mongo_context import MongoContext


class MongodbVerify(object):
    def __init__(self, mongo_client: MongoClient, mongo_context: MongoContext):
        self.__mongo_client = mongo_client
        self.__mongo_context = mongo_context

    def document_exists(self, database: str, collection: str, document: dict, num_expected: int = 1):
        """Returns True if a document exists in the given database and collection. If num_expected is set to None,
        any number of documents will be considered passing."""
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
