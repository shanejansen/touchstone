from touchstone.lib.nodes.deps.behaviors.i_behavior import IBehavior
from touchstone.lib.nodes.deps.i_dependency import IDependency
from touchstone.lib.nodes.deps.local.i_runnable_local import IRunnableLocal


class RunnableLocalDep(IDependency, IRunnableLocal):
    def __init__(self, name: str, pretty_name: str, runnable_local: IRunnableLocal):
        self.__name = name
        self.__pretty_name = pretty_name
        self.__runnable_local = runnable_local

    def get_name(self) -> str:
        return self.__name

    def get_pretty_name(self) -> str:
        return self.__pretty_name

    def get_behavior(self) -> IBehavior:
        return self.__runnable_local.get_behavior()

    def initialize(self):
        self.__runnable_local.initialize()

    def start(self):
        self.__runnable_local.start()

    def stop(self):
        self.__runnable_local.stop()

    def reset(self):
        self.__runnable_local.reset()

    def is_healthy(self) -> bool:
        return self.__runnable_local.is_healthy()
