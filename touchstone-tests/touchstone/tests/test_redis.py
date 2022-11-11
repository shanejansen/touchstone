import json

from touchstone.lib.touchstone_test import TouchstoneTest


class Set(TouchstoneTest):
    def given(self) -> object:
        pass

    def when(self, given) -> object:
        self.deps.redis.setup().set('foo', 'bar')
        return None

    def then(self, given, result) -> bool:
        return self.deps.redis.verify().value_matches('foo', 'bar')


class ValueExists(TouchstoneTest):
    def given(self) -> object:
        pass

    def when(self, given) -> object:
        self.deps.redis.setup().set('foo', 'bar')
        return None

    def then(self, given, result) -> bool:
        return self.deps.redis.verify().value_exists('foo')


class ValueMatches(TouchstoneTest):
    def given(self) -> object:
        pass

    def when(self, given) -> object:
        self.deps.redis.setup().set('foo', 'bar')
        return None

    def then(self, given, result) -> bool:
        return self.deps.redis.verify().value_matches('foo', 'bar')


class ValueMatchesJson(TouchstoneTest):
    def given(self) -> object:
        return {'foo': 'bar'}

    def when(self, given) -> object:
        self.deps.redis.setup().set('foo', json.dumps(given))
        return None

    def then(self, given, result) -> bool:
        return self.deps.redis.verify().value_matches_json('foo', given)
