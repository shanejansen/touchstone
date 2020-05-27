from touchstone.lib import exceptions
from touchstone.lib.mocks.configurers.i_configurable import IConfigurable
from touchstone.lib.mocks.runnables.filesystem.i_filesystem_behavior import IFilesystemBehavior, IFilesystemVerify, \
    IFilesystemSetup
from touchstone.lib.mocks.runnables.filesystem.local.local_filesystem_setup import LocalFilesystemSetup
from touchstone.lib.mocks.runnables.filesystem.local.local_filesystem_verify import LocalFilesystemVerify
from touchstone.lib.mocks.runnables.i_runnable import IRunnable


class LocalFilesystemRunnable(IRunnable, IFilesystemBehavior):
    def __init__(self, defaults_configurer: IConfigurable, base_files_path: str, setup: LocalFilesystemSetup,
                 verify: LocalFilesystemVerify):
        self.__defaults_configurer = defaults_configurer
        self.__base_files_path = base_files_path
        self.__setup = setup
        self.__verify = verify

    def start(self):
        self.__setup.init(self.__defaults_configurer.get_config())

    def stop(self):
        self.__setup.delete_defaults(self.__defaults_configurer.get_config())

    def reset(self):
        self.__setup.init(self.__defaults_configurer.get_config())

    def services_available(self):
        pass

    def setup(self) -> IFilesystemSetup:
        if not self.__setup:
            raise exceptions.MockException('Setup unavailable. Mock is still starting.')
        return self.__setup

    def verify(self) -> IFilesystemVerify:
        if not self.__verify:
            raise exceptions.MockException('Verify unavailable. Mock is still starting.')
        return self.__verify

    def get_base_path(self) -> str:
        return self.__base_files_path
