import abc

from touchstone.lib.nodes.deps.behaviors.i_behavior import IBehavior


class IRedisSetup(object):
    @abc.abstractmethod
    def set(self, key: str, value: str):
        """Sets a key-value pair."""
        pass


class IRedisVerify(object):
    @abc.abstractmethod
    def value_exists(self, key: str) -> bool:
        """Returns True if the given key exists."""
        pass

    @abc.abstractmethod
    def value_matches(self, key: str, value: str) -> bool:
        """Returns True if the given key matches the given value."""

    @abc.abstractmethod
    def value_matches_json(self, key: str, value: dict) -> bool:
        """Returns True if the given key matches the given JSON value."""


class IRedisBehavior(IBehavior):
    @abc.abstractmethod
    def setup(self) -> IRedisSetup:
        pass

    @abc.abstractmethod
    def verify(self) -> IRedisVerify:
        pass
