from pika.adapters.blocking_connection import BlockingChannel

from touchstone.lib.mocks.mock_case import Verify


class RabbitmqVerify(Verify):
    def __init__(self, channel: BlockingChannel):
        super().__init__()
        self.channel: BlockingChannel = channel
