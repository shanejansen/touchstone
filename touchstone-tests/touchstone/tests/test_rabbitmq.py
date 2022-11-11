from touchstone.lib.touchstone_test import TouchstoneTest


class MessagesPublished(TouchstoneTest):
    def processing_period(self) -> float:
        return 0.5

    def given(self) -> object:
        return None

    def when(self, given) -> object:
        self.deps.rabbitmq.setup().publish('default-direct.exchange', 'some payload')
        return None

    def then(self, given, result) -> bool:
        return self.deps.rabbitmq.verify().messages_published('default-direct.exchange')


class MessagesPublishedWithTimes(TouchstoneTest):
    def processing_period(self) -> float:
        return 0.5

    def given(self) -> object:
        return None

    def when(self, given) -> object:
        self.deps.rabbitmq.setup().publish('default-direct.exchange', 'some payload', 'foo')
        self.deps.rabbitmq.setup().publish('default-direct.exchange', 'some payload', 'foo')
        self.deps.rabbitmq.setup().publish('default-direct.exchange', 'some payload', 'foo')
        self.deps.rabbitmq.setup().publish('default-direct.exchange', 'some payload', 'bar')
        return None

    def then(self, given, result) -> bool:
        return self.deps.rabbitmq.verify().messages_published('default-direct.exchange', 3, 'foo')


class PayloadPublished(TouchstoneTest):
    def processing_period(self) -> float:
        return 0.5

    def given(self) -> object:
        return 'some payload'

    def when(self, given) -> object:
        self.deps.rabbitmq.setup().publish('default-topic.exchange', given, 'foo')
        return None

    def then(self, given, result) -> bool:
        return self.deps.rabbitmq.verify().payload_published('default-topic.exchange', given, 'foo')


class JsonPayloadPublished(TouchstoneTest):
    def processing_period(self) -> float:
        return 0.5

    def given(self) -> object:
        return {'foo': 'bar'}

    def when(self, given) -> object:
        self.deps.rabbitmq.setup().publish('default-direct.exchange', 'some payload', 'foo')
        self.deps.rabbitmq.setup().publish_json('default-direct.exchange', given, 'foo')
        self.deps.rabbitmq.setup().publish('default-direct.exchange', 'some other payload', 'foo')
        return None

    def then(self, given, result) -> bool:
        return self.deps.rabbitmq.verify().payload_published_json('default-direct.exchange', given, 'foo')


class SameExchangeDifferentRoutingKeys(TouchstoneTest):
    def processing_period(self) -> float:
        return 0.5

    def given(self) -> object:
        pass

    def when(self, given) -> object:
        self.deps.rabbitmq.setup().publish('my-exchange', 'foo', 'route.b')
        self.deps.rabbitmq.setup().publish('my-exchange', 'foo', 'route.b')
        return None

    def then(self, given, result) -> bool:
        return self.deps.rabbitmq.verify().messages_published('my-exchange', num_expected=2, routing_key='route.b')
