import urllib.error
import urllib.request
from typing import Optional

from minio import Minio

from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.mock import Mock
from touchstone.lib.mocks.mock_defaults import MockDefaults
from touchstone.lib.mocks.network import Network
from touchstone.lib.mocks.s3.s3_setup import S3Setup
from touchstone.lib.mocks.s3.s3_verify import S3Verify


class S3(Mock):
    __USERNAME = 'admin123'
    __PASSWORD = 'admin123'

    def __init__(self, host: str, mock_defaults: MockDefaults, docker_manager: DockerManager):
        super().__init__(host, mock_defaults)
        self.setup: S3Setup = None
        self.verify: S3Verify = None
        self.__docker_manager = docker_manager
        self.__container_id: Optional[str] = None

    @staticmethod
    def name() -> str:
        return 's3'

    @staticmethod
    def pretty_name() -> str:
        return 'S3'

    def run(self) -> Network:
        run_result = self.__docker_manager.run_image('minio/minio:RELEASE.2020-02-27T00-23-05Z server /data',
                                                     port=9000,
                                                     environment_vars=[('MINIO_ACCESS_KEY', self.__USERNAME),
                                                                       ('MINIO_SECRET_KEY', self.__PASSWORD)])
        self.__container_id = run_result.container_id
        return Network(internal_host=run_result.container_id,
                       internal_port=run_result.internal_port,
                       external_port=run_result.external_port,
                       username=self.__USERNAME,
                       password=self.__PASSWORD)

    def is_healthy(self) -> bool:
        try:
            response = urllib.request.urlopen(f'http://{self.network.external_url()}/minio/health/ready').read()
            return response is not None
        except (urllib.error.URLError, ConnectionResetError):
            return False

    def initialize(self):
        s3_client = Minio(self.network.external_url(),
                          access_key=self.__USERNAME,
                          secret_key=self.__PASSWORD,
                          secure=False)
        self.setup = S3Setup(s3_client)
        self.verify = S3Verify(s3_client)
        path = self._mock_defaults.path
        defaults = self._mock_defaults.get(self.name())
        self.setup.init(path, defaults)

    def reset(self):
        path = self._mock_defaults.path
        defaults = self._mock_defaults.get(self.name())
        self.setup.init(path, defaults)

    def stop(self):
        if self.__container_id:
            self.__docker_manager.stop_container(self.__container_id)
