from touchstone.lib.mocks.mock_case import Setup
from touchstone.lib.mocks.mock_context import MockContext


class RabbitmqSetup(Setup):
    def __init__(self, mock_context: MockContext):
        super().__init__(mock_context)

    def load_defaults(self, defaults: dict):
        pass

    def cleanup(self):
        pass
