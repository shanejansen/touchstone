import abc


class IFilesystemSetup(object):
    pass


class IFilesystemVerify(object):
    @abc.abstractmethod
    def file_exists(self, path: str) -> bool:
        pass

    @abc.abstractmethod
    def file_matches(self, path: str, expected: bytes) -> bool:
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
        pass
