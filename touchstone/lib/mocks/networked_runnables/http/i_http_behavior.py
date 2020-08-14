import abc


class IHttpSetup(object):
    @abc.abstractmethod
    def get(self, endpoint: str, response: str, response_status: int = 200,
            response_headers: dict = {'Content-Type': 'application/json'}):
        """Returns the given response when a GET request is made to the given endpoint."""
        pass

    @abc.abstractmethod
    def post(self, endpoint: str, response: str, response_status: int = 200,
             response_headers: dict = {'Content-Type': 'application/json'}):
        """Returns the given response when a POST request is made to the given endpoint."""
        pass

    @abc.abstractmethod
    def put(self, endpoint: str, response: str, response_status: int = 200,
            response_headers: dict = {'Content-Type': 'application/json'}):
        """Returns the given response when a PUT request is made to the given endpoint."""
        pass

    @abc.abstractmethod
    def delete(self, endpoint: str, response: str, response_status: int = 200,
               response_headers: dict = {'Content-Type': 'application/json'}):
        """Returns the given response when a DELETE request is made to the given endpoint."""
        pass


class IHttpVerify(object):
    @abc.abstractmethod
    def get_called(self, endpoint: str, times: int = 1) -> bool:
        """Returns True if the given endpoint has been called with a GET request the given number of times.
        If times is set to None, the endpoint can be called any number of times."""
        pass

    @abc.abstractmethod
    def post_called(self, endpoint: str, times: int = 1) -> bool:
        """Returns True if the given endpoint has been called with a POST request the given number of times.
        If times is set to None, the endpoint can be called any number of times."""
        pass

    @abc.abstractmethod
    def post_contained(self, endpoint: str, expected_body: str) -> bool:
        """Returns True if the given endpoint has been called with a POST request containing the given expected
        body."""
        pass

    @abc.abstractmethod
    def post_contained_json(self, endpoint: str, expected_body: dict) -> bool:
        """Returns True if the given endpoint has been called with a POST request containing the given expected
        JSON body."""
        pass

    @abc.abstractmethod
    def put_called(self, endpoint: str, times: int = 1) -> bool:
        """Returns True if the given endpoint has been called with a PUT request the given number of times.
        If times is set to None, the endpoint can be called any number of times."""
        pass

    @abc.abstractmethod
    def put_contained(self, endpoint: str, expected_body: str) -> bool:
        """Returns True if the given endpoint has been called with a PUT request containing the given expected
        body."""
        pass

    @abc.abstractmethod
    def put_contained_json(self, endpoint: str, expected_body: dict) -> bool:
        """Returns True if the given endpoint has been called with a PUT request containing the given expected
        JSON body."""
        pass

    @abc.abstractmethod
    def delete_called(self, endpoint: str, times: int = 1) -> bool:
        """Returns True if the given endpoint has been called with a DELETE request the given number of times.
        If times is set to None, the endpoint can be called any number of times."""
        pass

    @abc.abstractmethod
    def delete_contained(self, endpoint: str, expected_body: str) -> bool:
        """Returns True if the given endpoint has been called with a DELETE request containing the given expected
        body."""
        pass

    @abc.abstractmethod
    def delete_contained_json(self, endpoint: str, expected_body: dict) -> bool:
        """Returns True if the given endpoint has been called with a DELETE request containing the given expected
        JSON body."""
        pass


class IHttpBehavior(object):
    @abc.abstractmethod
    def setup(self) -> IHttpSetup:
        pass

    @abc.abstractmethod
    def verify(self) -> IHttpVerify:
        pass

    @abc.abstractmethod
    def url(self) -> str:
        """Returns the URL of this mocked HTTP resource."""
        pass
