import os

from touchstone.lib.mocks.runnables.filesystem.i_filesystem_behavior import IFilesystemVerify


class LocalFilesystemVerify(IFilesystemVerify):
    def __init__(self, base_files_path: str):
        self.__base_files_path = base_files_path

    def file_exists(self, path: str) -> bool:
        path = os.path.join(self.__base_files_path, path)
        exists = os.path.isfile(path)
        if not exists:
            print(f'Path: "{path}" does not exist.')
        return exists

    def file_matches(self, path: str, expected: bytes) -> bool:
        path = os.path.join(self.__base_files_path, path)
        with open(path, 'rb') as data:
            data_matches = bytes(data.read()) == expected
        if not data_matches:
            print('Expected data does not match data in object.')
        return data_matches
