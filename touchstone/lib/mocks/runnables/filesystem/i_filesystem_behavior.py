import abc


class IFilesystemSetup(object):
    pass


class IFilesystemVerify(object):
    @abc.abstractmethod
    def file_exists(self, path: str) -> bool:
        """Returns True if the given path to a file exists. Assumes "defaults" as a base directory."""
        pass

    @abc.abstractmethod
    def file_matches(self, path: str, expected: bytes) -> bool:
        """Returns True if the given path to a file matches the expected bytes.
        Assumes "defaults" as a base directory."""
        pass


class IFilesystemBehavior(object):
    @abc.abstractmethod
    def setup(self) -> IFilesystemSetup:
        pass

    @abc.abstractmethod
    def verify(self) -> IFilesystemVerify:
        pass

    @abc.abstractmethod
    def get_base_path(self) -> str:
        """Returns the "defaults" base directory path."""
        pass
