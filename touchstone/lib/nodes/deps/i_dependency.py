import abc

from touchstone.lib.nodes.deps.behaviors.i_behavior import IBehavior


class IDependency(object):
    @abc.abstractmethod
    def get_name(self) -> str:
        pass

    @abc.abstractmethod
    def get_pretty_name(self) -> str:
        pass

    @abc.abstractmethod
    def get_behavior(self) -> IBehavior:
        pass
