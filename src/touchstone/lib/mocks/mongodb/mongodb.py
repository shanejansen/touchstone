from typing import Optional

import pymongo

from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.mock import Mock
from touchstone.lib.mocks.mongodb.mongo_context import MongoContext
from touchstone.lib.mocks.mongodb.mongodb_setup import MongodbSetup
from touchstone.lib.mocks.mongodb.mongodb_verify import MongodbVerify
from touchstone.lib.mocks.run_context import RunContext


class Mongodb(Mock):
    def __init__(self, host: str, is_dev_mode: bool, docker_manager: DockerManager):
        super().__init__(host, is_dev_mode)
        self.setup: MongodbSetup = None
        self.verify: MongodbVerify = None
        self.__docker_manager = docker_manager
        self.__container_id: Optional[str] = None
        self.__ui_container_id: Optional[str] = None

    @staticmethod
    def name() -> str:
        return 'mongodb'

    @staticmethod
    def pretty_name() -> str:
        return 'Mongo DB'

    def is_healthy(self) -> bool:
        try:
            client = pymongo.MongoClient(self.run_context.host, self.run_context.port)
            status = client.admin.command('serverStatus')['ok']
            return status == 1.0
        except Exception:
            return False

    def run(self) -> RunContext:
        run_result = self.__docker_manager.run_image('mongo:4.0.14', (27017, 27017))
        self.__container_id = run_result.container_id

        ui_port = None
        if self._is_dev_mode:
            environment_vars = [('ME_CONFIG_MONGODB_PORT', run_result.port), ('ME_CONFIG_MONGODB_SERVER', self._host)]
            ui_run_result = self.__docker_manager.run_image('mongo-express:0.49.0', (27018, 8081),
                                                            environment_vars=environment_vars)
            self.__ui_container_id = ui_run_result.container_id
            ui_port = ui_run_result.port

        return RunContext(self._host, run_result.port, ui_port=ui_port)

    def initialize(self):
        mongo_client = pymongo.MongoClient(self.run_context.host, self.run_context.port)
        mongo_context = MongoContext()
        self.setup = MongodbSetup(mongo_client, mongo_context)
        self.verify = MongodbVerify(mongo_client, mongo_context)

    def stop(self):
        if self.__container_id:
            self.__docker_manager.stop_container(self.__container_id)
        if self.__ui_container_id:
            self.__docker_manager.stop_container(self.__ui_container_id)

    def load_defaults(self, defaults: dict):
        self.setup.load_defaults(defaults)

    def reset(self):
        self.setup.reset()
