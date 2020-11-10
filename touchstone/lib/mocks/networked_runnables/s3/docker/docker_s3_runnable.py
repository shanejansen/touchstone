from minio import Minio

from touchstone.lib import exceptions
from touchstone.lib.health_checks.http_health_check import HttpHealthCheck
from touchstone.lib.managers.docker_manager import DockerManager
from touchstone.lib.mocks.configurers.i_configurable import IConfigurable
from touchstone.lib.mocks.networked_runnables.i_networked_runnable import INetworkedRunnable
from touchstone.lib.mocks.networked_runnables.s3.docker.docker_s3_setup import DockerS3Setup
from touchstone.lib.mocks.networked_runnables.s3.docker.docker_s3_verify import DockerS3Verify
from touchstone.lib.mocks.networked_runnables.s3.i_s3_behavior import IS3Behavior, IS3Verify, IS3Setup
from touchstone.lib.networking.docker_network import DockerNetwork
from touchstone.lib.networking.i_network import INetwork


class DockerS3Runnable(INetworkedRunnable, IS3Behavior):
    __USERNAME = 'admin123'
    __PASSWORD = 'admin123'

    def __init__(self, defaults_configurer: IConfigurable, base_objects_path: str, health_check: HttpHealthCheck,
                 setup: DockerS3Setup, verify: DockerS3Verify, docker_manager: DockerManager,
                 docker_network: DockerNetwork):
        self.__defaults_configurer = defaults_configurer
        self.__base_objects_path = base_objects_path
        self.__health_check = health_check
        self.__setup = setup
        self.__verify = verify
        self.__docker_manager = docker_manager
        self.__docker_network = docker_network

    def get_network(self) -> INetwork:
        return self.__docker_network

    def initialize(self):
        s3_client = Minio(self.__docker_network.external_url(),
                          access_key=self.__USERNAME,
                          secret_key=self.__PASSWORD,
                          secure=False)
        self.__setup.set_s3_client(s3_client)
        self.__verify.set_s3_client(s3_client)
        self.__setup.init(self.__base_objects_path, self.__defaults_configurer.get_config())

    def start(self):
        run_result = self.__docker_manager.run_background_image('minio/minio:RELEASE.2020-02-27T00-23-05Z server /data',
                                                                port=9000,
                                                                environment_vars=[('MINIO_ACCESS_KEY', self.__USERNAME),
                                                                                  (
                                                                                      'MINIO_SECRET_KEY',
                                                                                      self.__PASSWORD)])
        self.__docker_network.set_container_id(run_result.container_id)
        self.__docker_network.set_internal_port(run_result.internal_port)
        self.__docker_network.set_external_port(run_result.external_port)
        self.__docker_network.set_ui_port(run_result.external_port)
        self.__docker_network.set_ui_endpoint('/minio')
        self.__docker_network.set_username(self.__USERNAME)
        self.__docker_network.set_password(self.__PASSWORD)

    def stop(self):
        if self.__docker_network.container_id():
            self.__docker_manager.stop_container(self.__docker_network.container_id())

    def reset(self):
        self.__setup.init(self.__base_objects_path, self.__defaults_configurer.get_config())

    def services_available(self):
        pass

    def is_healthy(self) -> bool:
        self.__health_check.set_url(self.__docker_network.ui_url() + '/health/ready')
        return self.__health_check.is_healthy()

    def setup(self) -> IS3Setup:
        if not self.__setup:
            raise exceptions.MockException('Setup unavailable. Mock is still starting.')
        return self.__setup

    def verify(self) -> IS3Verify:
        if not self.__verify:
            raise exceptions.MockException('Verify unavailable. Mock is still starting.')
        return self.__verify

    def get_base_path(self) -> str:
        return self.__base_objects_path
