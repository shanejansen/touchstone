import abc
from typing import Optional


class IFilesystemSetup(object):
    pass


class IFilesystemVerify(object):
    @abc.abstractmethod
    def file_exists(self, path: str, expected_num_files: int = 1) -> bool:
        """Returns True if the given path to a file exists. Assumes "touchstone/io" as a base directory. Wildcards may
        be used in path."""
        pass

    @abc.abstractmethod
    def file_matches(self, path: str, expected: bytes) -> bool:
        """Returns True if the given path to a file matches the expected bytes. Assumes "touchstone/io" as a base
        directory. Wildcards may be used in path."""
        pass

    @abc.abstractmethod
    def file_matches_json(self, path: str, expected: dict) -> bool:
        """Returns True if the given path to a file matches the expected JSON. Assumes "touchstone/io" as a base
        directory. Wildcards may be used in path."""
        pass

    @abc.abstractmethod
    def get_file_matching(self, path: str) -> Optional[str]:
        """Returns the path to a single file matching the given path including wildcards. Returns None if nothing
        found."""
        pass


class IFilesystemBehavior(object):
    @abc.abstractmethod
    def setup(self) -> IFilesystemSetup:
        pass

    @abc.abstractmethod
    def verify(self) -> IFilesystemVerify:
        pass

    @abc.abstractmethod
    def get_io_path(self) -> str:
        """Returns the path to the I/O files used by the service."""
        pass
