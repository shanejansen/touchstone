from touchstone.lib.mocks.mock_case import Verify
from touchstone.lib.mocks.mock_context import MockContext


class RabbitmqVerify(Verify):
    def __init__(self, mock_context: MockContext):
        super().__init__(mock_context)
