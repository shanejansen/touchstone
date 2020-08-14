import json

from minio import Minio

from touchstone.helpers import validation
from touchstone.lib.mocks.networked_runnables.s3.i_s3_behavior import IS3Verify


class DockerS3Verify(IS3Verify):
    def __init__(self):
        self.__s3_client = None

    def set_s3_client(self, s3_client: Minio):
        self.__s3_client = s3_client

    def bucket_exists(self, name: str) -> bool:
        return self.__s3_client.bucket_exists(name)

    def object_exists(self, bucket_name: str, object_name: str) -> bool:
        exists = self.__s3_client.stat_object(bucket_name, object_name)
        if not exists:
            print(f'Object name: "{object_name}" could not be found in bucket: "{bucket_name}"')
        return exists

    def object_matches(self, bucket_name: str, object_name: str, expected: bytes) -> bool:
        data = self.__s3_client.get_object(bucket_name, object_name).data
        data_matches = data == expected
        if not data_matches:
            print('Expected data does not match data in object.')
        return data_matches

    def object_matches_json(self, bucket_name: str, object_name: str, expected_json: dict) -> bool:
        data = self.__s3_client.get_object(bucket_name, object_name).data
        actual = json.loads(data.decode('utf-8'))
        return validation.matches(expected_json, actual)
