import abc


class IS3Setup(object):
    @abc.abstractmethod
    def create_bucket(self, name: str):
        """Creates a new bucket with the given name."""
        pass

    @abc.abstractmethod
    def put_object(self, bucket_name: str, object_name: str, data: bytes,
                   content_type: str = 'application/octet-stream'):
        """Puts the given bytes into a bucket and object."""
        pass

    @abc.abstractmethod
    def put_json_object(self, bucket_name: str, object_name: str, input_json: dict):
        """Puts the given JSON into a bucket and object."""
        pass


class IS3Verify(object):
    @abc.abstractmethod
    def bucket_exists(self, name: str) -> bool:
        """Return True if the given bucket name exists."""
        pass

    @abc.abstractmethod
    def object_exists(self, bucket_name: str, object_name: str) -> bool:
        """Returns True if the given bucket and object name exists."""
        pass

    @abc.abstractmethod
    def object_matches(self, bucket_name: str, object_name: str, expected: bytes) -> bool:
        """Returns True if the given object in a bucket matches the expected bytes."""
        pass

    @abc.abstractmethod
    def object_matches_json(self, bucket_name: str, object_name: str, expected_json: dict) -> bool:
        """Returns True if the given JSON object in a bucket matches the expected JSON."""
        pass


class IS3Behavior(object):
    @abc.abstractmethod
    def setup(self) -> IS3Setup:
        pass

    @abc.abstractmethod
    def verify(self) -> IS3Verify:
        pass

    @abc.abstractmethod
    def get_base_path(self) -> str:
        """Returns the "defaults" base directory path."""
        pass
