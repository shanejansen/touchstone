from typing import Optional

import pymongo

from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.mock import Mock
from touchstone.lib.mocks.mock_defaults import MockDefaults
from touchstone.lib.mocks.mongodb.mongo_context import MongoContext
from touchstone.lib.mocks.mongodb.mongodb_setup import MongodbSetup
from touchstone.lib.mocks.mongodb.mongodb_verify import MongodbVerify
from touchstone.lib.mocks.network import Network


class Mongodb(Mock):
    def __init__(self, host: str, mock_defaults: MockDefaults, is_dev_mode: bool, docker_manager: DockerManager):
        super().__init__(host, mock_defaults)
        self.setup: MongodbSetup = None
        self.verify: MongodbVerify = None
        self.__docker_manager = docker_manager
        self.__is_dev_mode = is_dev_mode
        self.__container_id: Optional[str] = None
        self.__ui_container_id: Optional[str] = None

    @staticmethod
    def name() -> str:
        return 'mongodb'

    @staticmethod
    def pretty_name() -> str:
        return 'Mongo DB'

    def run(self) -> Network:
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

        return Network(internal_host=run_result.container_id,
                       internal_port=run_result.internal_port,
                       external_port=run_result.external_port,
                       ui_port=ui_port)

    def is_healthy(self) -> bool:
        try:
            client = pymongo.MongoClient(self.network.external_host, self.network.external_port)
            status = client.admin.command('serverStatus')['ok']
            return status == 1.0
        except Exception:
            return False

    def initialize(self):
        mongo_client = pymongo.MongoClient(self.network.external_host, self.network.external_port)
        mongo_context = MongoContext()
        self.setup = MongodbSetup(mongo_client, mongo_context)
        self.verify = MongodbVerify(mongo_client, mongo_context)
        self.setup.init(self._mock_defaults.get(self.name()))

    def reset(self):
        self.setup.init(self._mock_defaults.get(self.name()))

    def stop(self):
        if self.__container_id:
            self.__docker_manager.stop_container(self.__container_id)
        if self.__ui_container_id:
            self.__docker_manager.stop_container(self.__ui_container_id)
