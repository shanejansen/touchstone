from touchstone.lib.mocks.mock_case import Exercise
from touchstone.lib.mocks.mock_context import MockContext


class HttpExercise(Exercise):
    def __init__(self, mock_context: MockContext):
        super().__init__(mock_context)
