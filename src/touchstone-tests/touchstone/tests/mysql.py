from touchstone.lib.touchstone_test import TouchstoneTest

mysql_database = 'myapp'
mysql_table = 'users'


class RowInserted(TouchstoneTest):
    def given(self) -> object:
        return {
            'first_name': 'Foo',
            'last_name': 'Bar'
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
                'first_name': 'Foo',
                'last_name': 'Bar'
            },
            {
                'first_name': 'Foo',
                'last_name': 'Bar'
            },
            {
                'first_name': 'Baz',
                'last_name': 'Qux'
            }
        ]

    def when(self, given) -> object:
        self.mocks.mysql.setup.insert_rows(mysql_database, mysql_table, given)
        return None

    def then(self, given, result) -> bool:
        expected_foo = {
            'first_name': 'Foo',
            'last_name': 'Bar'
        }
        expected_baz = {
            'first_name': 'Baz'
        }
        return self.mocks.mysql.verify.row_exists(mysql_database, mysql_table, expected_foo, num_expected=2) \
               and self.mocks.mysql.verify.row_exists(mysql_database, mysql_table, expected_baz)
