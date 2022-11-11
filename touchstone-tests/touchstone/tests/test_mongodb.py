from touchstone.lib.touchstone_test import TouchstoneTest

mongo_database = 'myapp'
mongo_collection = 'users'


class DocumentInserted(TouchstoneTest):
    def given(self) -> object:
        return {
            'firstName': 'Foo',
            'lastName': 'Bar'
        }

    def when(self, given) -> object:
        self.deps.mongodb.setup().insert_document(mongo_database, mongo_collection, given)
        return None

    def then(self, given, result) -> bool:
        return self.deps.mongodb.verify().document_exists(mongo_database, mongo_collection, given)


class DocumentsInserted(TouchstoneTest):
    def given(self) -> object:
        return [
            {
                'firstName': 'Foo',
                'lastName': 'Bar'
            },
            {
                'firstName': 'Foo',
                'lastName': 'Bar'
            },
            {
                'firstName': 'Baz',
                'lastName': 'Qux'
            }
        ]

    def when(self, given) -> object:
        self.deps.mongodb.setup().insert_documents(mongo_database, mongo_collection, given)
        return None

    def then(self, given, result) -> bool:
        expected_foo = {
            'firstName': 'Foo',
            'lastName': 'Bar'
        }
        expected_baz = {
            'firstName': 'Baz'
        }
        return self.deps.mongodb.verify().document_exists(mongo_database, mongo_collection, expected_foo,
                                                           num_expected=2) \
               and self.deps.mongodb.verify().document_exists(mongo_database, mongo_collection, expected_baz)
