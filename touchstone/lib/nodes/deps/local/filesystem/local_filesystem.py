from touchstone.lib import exceptions
from touchstone.lib.configurers.i_configurable import IConfigurable
from touchstone.lib.nodes.deps.behaviors.i_behavior import IBehavior
from touchstone.lib.nodes.deps.behaviors.i_filesystem_behavior import IFilesystemBehavior, IFilesystemVerify, \
    IFilesystemSetup
from touchstone.lib.nodes.deps.local.filesystem.local_filesystem_setup import LocalFilesystemSetup
from touchstone.lib.nodes.deps.local.filesystem.local_filesystem_verify import LocalFilesystemVerify
from touchstone.lib.nodes.deps.local.i_runnable_local import IRunnableLocal


class LocalFilesystem(IRunnableLocal, IFilesystemBehavior):
    def __init__(self, defaults_configurer: IConfigurable, files_path: str, setup: LocalFilesystemSetup,
                 verify: LocalFilesystemVerify):
        self.__defaults_configurer = defaults_configurer
        self.__files_path = files_path
        self.__setup = setup
        self.__verify = verify

    def get_behavior(self) -> IBehavior:
        return self

    def initialize(self):
        pass

    def start(self):
        self.__setup.reset()

    def stop(self):
        self.__setup.delete_defaults()

    def reset(self):
        self.__setup.reset()

    def is_healthy(self) -> bool:
        return True

    def setup(self) -> IFilesystemSetup:
        if not self.__setup:
            raise exceptions.DepException('Setup unavailable. Dependency is still starting.')
        return self.__setup

    def verify(self) -> IFilesystemVerify:
        if not self.__verify:
            raise exceptions.DepException('Verify unavailable. Dependency is still starting.')
        return self.__verify

    def get_io_path(self) -> str:
        return self.__files_path
