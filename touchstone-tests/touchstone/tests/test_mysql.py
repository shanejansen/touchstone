from touchstone.helpers import validation
from touchstone.lib.touchstone_test import TouchstoneTest

mysql_database = 'myapp'
mysql_table = 'users'


class RowInserted(TouchstoneTest):
    def given(self) -> object:
        return {
            'firstName': 'Foo',
            'lastName': 'Bar'
        }

    def when(self, given) -> object:
        self.deps.mysql.setup().insert_row(mysql_database, mysql_table, given)
        return None

    def then(self, given, result) -> bool:
        return self.deps.mysql.verify().row_exists(mysql_database, mysql_table, given)


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
        self.deps.mysql.setup().insert_rows(mysql_database, mysql_table, given)
        return None

    def then(self, given, result) -> bool:
        expected_foo = {
            'firstName': 'Foo',
            'lastName': 'Bar'
        }
        expected_baz = {
            'firstName': 'Baz'
        }
        return self.deps.mysql.verify().row_exists(mysql_database, mysql_table, expected_foo, num_expected=2) \
               and self.deps.mysql.verify().row_exists(mysql_database, mysql_table, expected_baz)


class NullValueInserted(TouchstoneTest):
    def given(self) -> object:
        return {
            'firstName': 'Foo',
            'lastName': None
        }

    def when(self, given) -> object:
        self.deps.mysql.setup().insert_row(mysql_database, mysql_table, given)
        return None

    def then(self, given, result) -> bool:
        return self.deps.mysql.verify().row_exists(mysql_database, mysql_table, given)


class CheckNotNull(TouchstoneTest):
    def given(self) -> object:
        return {
            'firstName': 'Foo',
            'lastName': 'Bar'
        }

    def when(self, given) -> object:
        self.deps.mysql.setup().insert_row(mysql_database, mysql_table, given)
        return None

    def then(self, given, result) -> bool:
        check = {
            'firstName': 'Foo',
            'lastName': validation.ANY
        }
        return self.deps.mysql.verify().row_exists(mysql_database, mysql_table, check)
