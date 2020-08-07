import os

from touchstone.lib.touchstone_test import TouchstoneTest


class FileExists(TouchstoneTest):
    def given(self) -> object:
        return os.path.join('some-dir', 'foo.csv')

    def when(self, given) -> object:
        return None

    def then(self, given, result) -> bool:
        return self.mocks.filesystem.verify().file_exists(given)


class FileExistsWithWildcard(TouchstoneTest):
    def given(self) -> object:
        return os.path.join('some-dir', '*.csv')

    def when(self, given) -> object:
        return None

    def then(self, given, result) -> bool:
        return self.mocks.filesystem.verify().file_exists(given, expected_num_files=2)


class FileMatches(TouchstoneTest):
    def given(self) -> object:
        path = os.path.join(self.mocks.filesystem.get_io_path(), 'some-dir', 'foo.csv')
        with open(path, 'rb') as data:
            return bytes(data.read())

    def when(self, given) -> object:
        return None

    def then(self, given, result) -> bool:
        path = os.path.join('some-dir', 'sub-dir', 'foo.csv')
        return self.mocks.filesystem.verify().file_matches(path, given)


class FileMatchesWithWildcard(TouchstoneTest):
    def given(self) -> object:
        path = os.path.join(self.mocks.filesystem.get_io_path(), 'some-dir', 'foo.csv')
        with open(path, 'rb') as data:
            return bytes(data.read())

    def when(self, given) -> object:
        return None

    def then(self, given, result) -> bool:
        path = os.path.join('some-dir', 'sub-dir', '*.csv')
        return self.mocks.filesystem.verify().file_matches(path, given)
