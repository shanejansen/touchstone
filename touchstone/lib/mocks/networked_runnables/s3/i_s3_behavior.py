import abc


class IS3Setup(object):
    @abc.abstractmethod
    def create_bucket(self, name: str):
        pass

    @abc.abstractmethod
    def put_object(self, bucket_name: str, object_name: str, data: bytes,
                   content_type: str = 'application/octet-stream'):
        pass


class IS3Verify(object):
    @abc.abstractmethod
    def bucket_exists(self, name: str) -> bool:
        pass

    @abc.abstractmethod
    def object_exists(self, bucket_name: str, object_name: str) -> bool:
        pass

    @abc.abstractmethod
    def object_matches(self, bucket_name: str, object_name: str, expected: bytes) -> bool:
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
        pass
