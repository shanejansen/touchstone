import glob
import json
import os
from typing import Optional

from touchstone.helpers import validation
from touchstone.lib.mocks.runnables.filesystem.i_filesystem_behavior import IFilesystemVerify


class LocalFilesystemVerify(IFilesystemVerify):
    def __init__(self, files_path: str):
        self.__files_path = files_path

    def file_exists(self, path: str, expected_num_files: int = 1) -> bool:
        path = os.path.join(self.__files_path, path)
        actual_num_files = len(glob.glob(path))
        if expected_num_files != actual_num_files:
            print(f'Expected number of files: "{expected_num_files}" does not match actual: "{actual_num_files}" '
                  f'at path: "{path}".')
            return False
        return True

    def file_matches(self, path: str, expected: bytes) -> bool:
        path = self.get_file_matching(path)
        if not path:
            print(f'Expected exactly 1 matching file at: "{path}".')
            return False
        with open(path, 'rb') as data:
            data_matches = bytes(data.read()) == expected
        if not data_matches:
            print('Expected data does not match data in file.')
        return data_matches

    def file_matches_json(self, path: str, expected: dict) -> bool:
        path = self.get_file_matching(path)
        if not path:
            print(f'Expected exactly 1 matching file at: "{path}".')
            return False
        with open(path, 'rb') as data:
            actual = json.loads(data.read().decode('utf-8'))
        return validation.matches(expected, actual)

    def get_file_matching(self, path: str) -> Optional[str]:
        path = os.path.join(self.__files_path, path)
        all_files = glob.glob(path)
        if len(all_files) != 1:
            return None
        return all_files[0]
