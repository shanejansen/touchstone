from touchstone.helpers import validation
from touchstone.lib.touchstone_test import TouchstoneTest

postgres_database = 'myapp'
postgres_table = 'users'


class RowInserted(TouchstoneTest):
    def given(self) -> object:
        return {
            'firstName': 'Foo',
            'lastName': 'Bar'
        }

    def when(self, given) -> object:
        self.deps.postgres.setup().insert_row(postgres_database, postgres_table, given)
        return None

    def then(self, given, result) -> bool:
        return self.deps.postgres.verify().row_exists(postgres_database, postgres_table, given)


class RowsInserted(TouchstoneTest):
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
        self.deps.postgres.setup().insert_rows(postgres_database, postgres_table, given)
        return None

    def then(self, given, result) -> bool:
        expected_foo = {
            'firstName': 'Foo',
            'lastName': 'Bar'
        }
        expected_baz = {
            'firstName': 'Baz'
        }
        return self.deps.postgres.verify().row_exists(postgres_database, postgres_table, expected_foo, num_expected=2) \
               and self.deps.postgres.verify().row_exists(postgres_database, postgres_table, expected_baz)


class NullValueInserted(TouchstoneTest):
    def given(self) -> object:
        return {
            'firstName': 'Foo',
            'lastName': None
        }

    def when(self, given) -> object:
        self.deps.postgres.setup().insert_row(postgres_database, postgres_table, given)
        return None

    def then(self, given, result) -> bool:
        return self.deps.postgres.verify().row_exists(postgres_database, postgres_table, given)


class CheckNotNull(TouchstoneTest):
    def given(self) -> object:
        return {
            'firstName': 'Foo',
            'lastName': 'Bar'
        }

    def when(self, given) -> object:
        self.deps.postgres.setup().insert_row(postgres_database, postgres_table, given)
        return None

    def then(self, given, result) -> bool:
        check = {
            'firstName': 'Foo',
            'lastName': validation.ANY
        }
        return self.deps.postgres.verify().row_exists(postgres_database, postgres_table, check)
