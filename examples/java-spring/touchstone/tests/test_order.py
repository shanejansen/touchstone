import json
from tests import creds
from touchstone.lib.touchstone_test import TouchstoneTest


class OrderMessageReceived(TouchstoneTest):
    """
    GIVEN an order.
    WHEN the given order is submitted to the 'order-placed.exchange'.
    THEN a mongo document should exist with that order.
    """

    def processing_period(self) -> float:
        return 0.5

    def given(self) -> object:
        return {
            'userId': 1,
            'item': 'Foo',
            'quantity': 2
        }

    def when(self, given) -> object:
        self.deps.rabbitmq.setup().publish('order-placed.exchange', json.dumps(given))
        return None

    def then(self, given, result) -> bool:
        return self.deps.mongodb.verify().document_exists(creds.MONGO_DATABASE, creds.MONGO_COLLECTION, given)
