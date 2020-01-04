from typing import Optional

import pymongo

from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.mock import Mock
from touchstone.lib.mocks.mongodb.mongo_context import MongoContext
from touchstone.lib.mocks.mongodb.mongodb_setup import MongodbSetup
from touchstone.lib.mocks.mongodb.mongodb_verify import MongodbVerify


class Mongodb(Mock):
    def __init__(self, default_host: str, docker_manager: DockerManager):
        super().__init__(default_host)
        self.setup: MongodbSetup = None
        self.verify: MongodbVerify = None
        self.__docker_manager = docker_manager
        self.__container_name: Optional[str] = None
        self.__ui_container_name: Optional[str] = None

    @staticmethod
    def name() -> str:
        return 'mongodb'

    @staticmethod
    def pretty_name() -> str:
        return 'Mongo DB'

    def default_port(self) -> int:
        return 27017

    def ui_port(self) -> int:
        return 27018

    def is_healthy(self) -> bool:
        try:
            client = pymongo.MongoClient(self.default_host(), self.default_port())
            status = client.admin.command('serverStatus')['ok']
            return status == 1.0
        except Exception:
            return False

    def start(self):
        self.__container_name = self.__docker_manager.run_image('mongo:4.0.14', [(self.default_port(), 27017)])
        environment_vars = [('ME_CONFIG_MONGODB_PORT', self.default_port()),
                            ('ME_CONFIG_MONGODB_SERVER', self.default_host())]
        self.__ui_container_name = self.__docker_manager.run_image('mongo-express:0.49.0',
                                                                   [(self.ui_port(), 8081)],
                                                                   environment_vars=environment_vars)

    def initialize(self):
        mongo_client = pymongo.MongoClient(self.default_host(), self.default_port())
        mongo_context = MongoContext()
        self.setup = MongodbSetup(mongo_client, mongo_context)
        self.verify = MongodbVerify(mongo_client, mongo_context)

    def stop(self):
        if self.__container_name:
            self.__docker_manager.stop_container(self.__container_name)
        if self.__ui_container_name:
            self.__docker_manager.stop_container(self.__ui_container_name)

    def load_defaults(self, defaults: dict):
        self.setup.load_defaults(defaults)

    def reset(self):
        self.setup.reset()
