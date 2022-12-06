import os

from touchstone.lib.touchstone_test import TouchstoneTest


class FileExists(TouchstoneTest):
    def given(self) -> object:
        return os.path.join('some-dir', 'foo.csv')

    def when(self, given) -> object:
        return None

    def then(self, given, result) -> bool:
        return self.deps.filesystem.verify().file_exists(given)


class FileExistsWithWildcard(TouchstoneTest):
    def given(self) -> object:
        return os.path.join('some-dir', '*.csv')

    def when(self, given) -> object:
        return None

    def then(self, given, result) -> bool:
        return self.deps.filesystem.verify().file_exists(given, expected_num_files=2)


class FileMatches(TouchstoneTest):
    def given(self) -> object:
        path = os.path.join(self.deps.filesystem.get_io_path(), 'some-dir', 'foo.csv')
        with open(path, 'rb') as data:
            return bytes(data.read())

    def when(self, given) -> object:
        return None

    def then(self, given, result) -> bool:
        path = os.path.join('some-dir', 'sub-dir', 'foo.csv')
        return self.deps.filesystem.verify().file_matches(path, given)


class FileMatchesJson(TouchstoneTest):
    def given(self) -> object:
        return {'foo': 'bar'}

    def when(self, given) -> object:
        return None

    def then(self, given, result) -> bool:
        path = os.path.join('some-dir', 'bar.json')
        return self.deps.filesystem.verify().file_matches_json(path, given)


class FileMatchesWithWildcard(TouchstoneTest):
    def given(self) -> object:
        path = os.path.join(self.deps.filesystem.get_io_path(), 'some-dir', 'foo.csv')
        with open(path, 'rb') as data:
            return bytes(data.read())

    def when(self, given) -> object:
        return None

    def then(self, given, result) -> bool:
        path = os.path.join('some-dir', 'sub-dir', '*.csv')
        return self.deps.filesystem.verify().file_matches(path, given)
