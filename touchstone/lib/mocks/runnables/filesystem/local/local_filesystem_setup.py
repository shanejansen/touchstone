import os
import shutil

from touchstone.lib.mocks.runnables.filesystem.i_filesystem_behavior import IFilesystemSetup


class LocalFilesystemSetup(IFilesystemSetup):
    def __init__(self, base_files_path: str):
        self.__base_files_path = base_files_path

    def init(self, defaults: dict):
        self.delete_defaults(defaults)
        for directory in defaults.get('directories', []):
            directory_path = os.path.join(self.__base_files_path, directory['path'])
            os.mkdir(directory_path)
            for file in directory.get('files', []):
                file_path = os.path.join(self.__base_files_path, file)
                shutil.copyfile(file_path, os.path.join(directory_path, os.path.basename(file_path)))

    def delete_defaults(self, defaults: dict):
        for directory in defaults.get('directories', []):
            path = os.path.join(self.__base_files_path, directory['path'])
            shutil.rmtree(path, ignore_errors=True)
