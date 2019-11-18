from mocks.mock_case import Verify


class HttpVerify(Verify):
    def __init__(self, exposed_port: int):
        super().__init__(exposed_port)
