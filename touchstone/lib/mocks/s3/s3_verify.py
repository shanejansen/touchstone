from minio import Minio


class S3Verify(object):
    def __init__(self, s3_client: Minio):
        self.__s3_client = s3_client

    def bucket_exists(self, name: str) -> bool:
        return self.__s3_client.bucket_exists(name)

    def object_exists(self, bucket_name: str, object_name: str) -> bool:
        return not self.__s3_client.stat_object(bucket_name, object_name)

    def object_matches(self, bucket_name: str, object_name: str, expected: bytes) -> bool:
        data = self.__s3_client.get_object(bucket_name, object_name).data
        return data == expected
