import pymongo

from touchstone.lib import exceptions
from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.network import Network
from touchstone.lib.mocks.networked_runnables.i_networked_runnable import INetworkedRunnable
from touchstone.lib.mocks.networked_runnables.mongodb.i_mongodb_behavior import IMongodbBehavior
from touchstone.lib.mocks.networked_runnables.mongodb.mongo_context import MongoContext
from touchstone.lib.mocks.networked_runnables.mongodb.mongodb_setup import MongodbSetup
from touchstone.lib.mocks.networked_runnables.mongodb.mongodb_verify import MongodbVerify


class MongodbRunnable(INetworkedRunnable, IMongodbBehavior):
    def __init__(self, defaults: dict, is_dev_mode: bool, docker_manager: DockerManager):
        self.__defaults = defaults
        self.__is_dev_mode = is_dev_mode
        self.__docker_manager = docker_manager
        self.__network = None
        self.__setup = None
        self.__verify = None
        self.__container_id = None
        self.__ui_container_id = None

    def get_network(self) -> Network:
        if not self.__network:
            raise exceptions.MockException('Network unavailable. Mock is still starting.')
        return self.__network

    def initialize(self):
        mongo_client = pymongo.MongoClient(self.get_network().external_host, self.get_network().external_port)
        mongo_context = MongoContext()
        self.__setup = MongodbSetup(mongo_client, mongo_context)
        self.__verify = MongodbVerify(mongo_client, mongo_context)
        self.__setup.init(self.__defaults)

    def start(self):
        run_result = self.__docker_manager.run_image('mongo:4.0.14', port=27017)
        self.__container_id = run_result.container_id

        ui_port = None
        if self.__is_dev_mode:
            ui_run_result = self.__docker_manager.run_image('mongo-express:0.49.0',
                                                            ui_port=8081,
                                                            environment_vars=[
                                                                ('ME_CONFIG_MONGODB_PORT', run_result.internal_port),
                                                                ('ME_CONFIG_MONGODB_SERVER', run_result.container_id)])
            self.__ui_container_id = ui_run_result.container_id
            ui_port = ui_run_result.ui_port

        self.__network = Network(internal_host=run_result.container_id,
                                 internal_port=run_result.internal_port,
                                 external_port=run_result.external_port,
                                 ui_port=ui_port)

    def stop(self):
        if self.__container_id:
            self.__docker_manager.stop_container(self.__container_id)
        if self.__ui_container_id:
            self.__docker_manager.stop_container(self.__ui_container_id)

    def reset(self):
        self.__setup.init(self.__defaults)

    def services_available(self):
        pass

    def is_healthy(self) -> bool:
        try:
            client = pymongo.MongoClient(self.get_network().external_host, self.get_network().external_port)
            status = client.admin.command('serverStatus')['ok']
            return status == 1.0
        except Exception:
            return False

    def setup(self) -> MongodbSetup:
        if not self.__setup:
            raise exceptions.MockException('Setup unavailable. Mock is still starting.')
        return self.__setup

    def verify(self) -> MongodbVerify:
        if not self.__verify:
            raise exceptions.MockException('Verify unavailable. Mock is still starting.')
        return self.__verify
