import json
import os
from io import BytesIO

from minio import Minio

from touchstone.lib.mocks.networked_runnables.s3.i_s3_behavior import IS3Setup


class DockerS3Setup(IS3Setup):
    def __init__(self):
        self.__s3_client = None

    def set_s3_client(self, s3_client: Minio):
        self.__s3_client = s3_client

    def init(self, path: str, defaults: dict):
        for bucket in self.__s3_client.list_buckets():
            objects = self.__s3_client.list_objects(bucket.name, recursive=True)
            for m_object in objects:
                self.__s3_client.remove_object(bucket.name, m_object.object_name)
            self.__s3_client.remove_bucket(bucket.name)

        for bucket in defaults.get('buckets', []):
            bucket_name = bucket['name']
            self.__s3_client.make_bucket(bucket_name)
            for m_object in bucket.get('objects', []):
                object_path = os.path.join(path, m_object['path'])
                file_stat = os.stat(object_path)
                with open(object_path, 'rb') as data:
                    self.__s3_client.put_object(
                        bucket_name,
                        m_object['name'],
                        data,
                        file_stat.st_size,
                        m_object['content-type']
                    )

    def create_bucket(self, name: str):
        self.__s3_client.make_bucket(name)

    def put_object(self, bucket_name: str, object_name: str, data: bytes,
                   content_type: str = 'application/octet-stream'):
        length = len(data)
        data = BytesIO(data)
        self.__s3_client.put_object(bucket_name, object_name, data, length, content_type)

    def put_json_object(self, bucket_name: str, object_name: str, input_json: dict):
        input_bytes = bytes(json.dumps(input_json), encoding='utf-8')
        self.put_object(bucket_name, object_name, input_bytes, 'application/json')
