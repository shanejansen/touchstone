class NotMockedException(Exception):
    def __init__(self, mock):
        super().__init__(f'{mock} was not specified as a mock. Please check your touchstone.json file.')


class MockNotSupportedException(Exception):
    pass


class ContainerException(Exception):
    pass
