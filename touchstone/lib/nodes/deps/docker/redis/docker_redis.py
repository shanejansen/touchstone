from redis import Redis

from touchstone.lib import exceptions
from touchstone.lib.configurers.i_configurable import IConfigurable
from touchstone.lib.managers.docker_manager import DockerManager
from touchstone.lib.networking.docker_network import DockerNetwork
from touchstone.lib.networking.i_network import INetwork
from touchstone.lib.nodes.deps.behaviors.i_behavior import IBehavior
from touchstone.lib.nodes.deps.behaviors.i_redis_behavior import IRedisBehavior, IRedisSetup, IRedisVerify
from touchstone.lib.nodes.deps.docker.i_runnable_docker import IRunnableDocker
from touchstone.lib.nodes.deps.docker.redis.docker_redis_setup import DockerRedisSetup
from touchstone.lib.nodes.deps.docker.redis.docker_redis_verify import DockerRedisVerify


class DockerRedis(IRunnableDocker, IRedisBehavior):
    def __init__(self, defaults_configurer: IConfigurable, is_dev_mode: bool, setup: DockerRedisSetup,
                 verify: DockerRedisVerify, docker_manager: DockerManager, docker_network: DockerNetwork):
        self.__defaults_configurer = defaults_configurer
        self.__is_dev_mode = is_dev_mode
        self.__setup = setup
        self.__verify = verify
        self.__docker_manager = docker_manager
        self.__docker_network = docker_network
        self.__ui_container_id = None

    def get_behavior(self) -> IBehavior:
        return self

    def get_network(self) -> INetwork:
        return self.__docker_network

    def initialize(self):
        redis_client = Redis(self.__docker_network.external_host(), self.__docker_network.external_port())
        self.__setup.set_redis_client(redis_client)
        self.__verify.set_redis_client(redis_client)
        self.__setup.init(self.__defaults_configurer.get_config())

    def start(self):
        run_result = self.__docker_manager.run_background_image('redis:6.2.5-alpine', port=6379)
        self.__docker_network.set_container_id(run_result.container_id)
        if self.__is_dev_mode:
            ui_run_result = self.__docker_manager.run_background_image(
                'rediscommander/redis-commander:redis-commander-210', ui_port=8081,
                environment_vars=[('REDIS_HOST', self.__docker_network.internal_host())])
            self.__ui_container_id = ui_run_result.container_id
            self.__docker_network.set_ui_port(ui_run_result.ui_port)
        self.__docker_network.set_internal_port(run_result.internal_port)
        self.__docker_network.set_external_port(run_result.external_port)

    def stop(self):
        if self.__docker_network.container_id():
            self.__docker_manager.stop_container(self.__docker_network.container_id())
        if self.__ui_container_id:
            self.__docker_manager.stop_container(self.__ui_container_id)

    def reset(self):
        self.__setup.init(self.__defaults_configurer.get_config())

    def is_healthy(self) -> bool:
        try:
            client = Redis(self.__docker_network.external_host(), self.__docker_network.external_port())
            client.info()
            return True
        except Exception:
            return False

    def setup(self) -> IRedisSetup:
        if not self.__setup:
            raise exceptions.DepException('Setup unavailable. Dependency is still starting.')
        return self.__setup

    def verify(self) -> IRedisVerify:
        if not self.__verify:
            raise exceptions.DepException('Verify unavailable. Dependency is still starting.')
        return self.__verify
