import os

from touchstone.lib.touchstone_test import TouchstoneTest


class FileExists(TouchstoneTest):
    def given(self) -> object:
        return './filesystem/some-dir/foo.csv'

    def when(self, given) -> object:
        return None

    def then(self, given, result) -> bool:
        return self.mocks.filesystem.verify().file_exists(given)


class FileMatches(TouchstoneTest):
    def given(self) -> object:
        path = os.path.join(self.mocks.filesystem.get_base_path(), './filesystem/some-dir/sub-dir/foo.csv')
        with open(path, 'rb') as data:
            return bytes(data.read())

    def when(self, given) -> object:
        return None

    def then(self, given, result) -> bool:
        return self.mocks.filesystem.verify().file_matches('./filesystem/some-dir/sub-dir/foo.csv', given)
