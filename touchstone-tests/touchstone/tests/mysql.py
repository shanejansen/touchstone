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
        self.mocks.mysql.setup.insert_row(mysql_database, mysql_table, given)
        return None

    def then(self, given, result) -> bool:
        return self.mocks.mysql.verify.row_exists(mysql_database, mysql_table, given)


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
        self.mocks.mysql.setup.insert_rows(mysql_database, mysql_table, given)
        return None

    def then(self, given, result) -> bool:
        expected_foo = {
            'firstName': 'Foo',
            'lastName': 'Bar'
        }
        expected_baz = {
            'firstName': 'Baz'
        }
        return self.mocks.mysql.verify.row_exists(mysql_database, mysql_table, expected_foo, num_expected=2) \
               and self.mocks.mysql.verify.row_exists(mysql_database, mysql_table, expected_baz)
