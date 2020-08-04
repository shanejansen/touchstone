import csv
import os

from touchstone.lib.touchstone_test import TouchstoneTest


class OutputCsvMatch(TouchstoneTest):
    def given(self) -> object:
        csv_path = os.path.join(self.mocks.filesystem.get_io_path(), 'emails.csv')
        with open(csv_path, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'email'])
            writer.writerow(['John', 'john@example.com'])
            writer.writerow(['Jane', 'jane@example.com'])
        self.mocks.mysql.setup().insert_rows('myapp', 'numbers', [
            {
                'name': 'John',
                'number': '5555551234'
            },
            {
                'name': 'Jane',
                'number': '5555555678'
            }
        ])
        return None

    def when(self, given) -> object:
        self.service_executor.execute('my-exec')
        return None

    def then(self, given, result) -> bool:
        path = os.path.join('output', '*.csv')
        expected_path = os.path.join(self.mocks.filesystem.get_io_path(), 'expected.csv')
        with open(expected_path, 'rb') as data:
            expected = bytes(data.read())
        return self.mocks.filesystem.verify().file_matches(path, expected)
