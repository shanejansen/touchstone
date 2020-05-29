import abc
from typing import List


class IMongodbSetup(object):
    def command(self, database: str, command: dict):
        """Execute an arbitrary command on the database."""
        pass

    def insert_document(self, database: str, collection: str, document: dict):
        """Inserts a document into the given database and collection."""
        pass

    def insert_documents(self, database: str, collection: str, documents: List[dict]):
        """Inserts multiple documents into the given database and collection."""
        pass


class IMongodbVerify(object):
    def document_exists(self, database: str, collection: str, document: dict, num_expected: int = 1) -> bool:
        """Returns True if a document exists in the given database and collection. If num_expected is set to None,
        any number of documents will be considered passing."""
        pass


class IMongodbBehavior(object):
    @abc.abstractmethod
    def setup(self) -> IMongodbSetup:
        pass

    @abc.abstractmethod
    def verify(self) -> IMongodbVerify:
        pass
