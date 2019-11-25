from lib.mocks.mock_case import Exercise


class HttpExercise(Exercise):
    def __init__(self, exposed_port: int):
        super().__init__(exposed_port)
