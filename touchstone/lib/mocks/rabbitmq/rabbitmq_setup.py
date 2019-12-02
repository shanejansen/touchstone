import asyncio

import aio_pika

from touchstone.lib.mocks.mock_case import Setup
from touchstone.lib.mocks.mock_context import MockContext


class RabbitmqSetup(Setup):
    def __init__(self, mock_context: MockContext):
        super().__init__(mock_context)

    def load_defaults(self, defaults: dict):
        pass

    def cleanup(self):
        pass

    def listen(self, exchange: str):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__listen(loop, exchange))
        loop.close()

    async def __listen(self, loop, exchange: str):
        connection = await aio_pika.connect_robust(
            "amqp://guest:guest@127.0.0.1/", loop=loop
        )
        queue_name = "test_queue"
