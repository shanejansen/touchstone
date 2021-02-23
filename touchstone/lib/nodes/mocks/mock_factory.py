import os
from typing import Optional

from touchstone.lib.configurers.BasicConfigurer import BasicConfigurer
from touchstone.lib.configurers.FileConfigurer import FileConfigurer
from touchstone.lib.health_checks.http_health_check import HttpHealthCheck
from touchstone.lib.managers.docker_manager import DockerManager
from touchstone.lib.networking.docker_network import DockerNetwork
from touchstone.lib.nodes.mocks.behaviors.i_mysql_behabior import IMysqlBehavior
from touchstone.lib.nodes.mocks.behaviors.i_rabbitmq_behavior import IRabbitmqBehavior
from touchstone.lib.nodes.mocks.docker.http.docker_http import DockerHttp
from touchstone.lib.nodes.mocks.docker.http.docker_http_setup import DockerHttpSetup
from touchstone.lib.nodes.mocks.docker.http.docker_http_verify import DockerHttpVerify
from touchstone.lib.nodes.mocks.docker.mongodb.docker_mongo_context import DockerMongoContext
from touchstone.lib.nodes.mocks.docker.mongodb.docker_mongodb import DockerMongodb
from touchstone.lib.nodes.mocks.docker.mongodb.docker_mongodb_setup import DockerMongodbSetup
from touchstone.lib.nodes.mocks.docker.mongodb.docker_mongodb_verify import DockerMongodbVerify
from touchstone.lib.nodes.mocks.docker.mysql.docker_mysql import DockerMysql
from touchstone.lib.nodes.mocks.docker.mysql.docker_mysql_context import DockerMysqlContext
from touchstone.lib.nodes.mocks.docker.mysql.docker_mysql_setup import DockerMysqlSetup
from touchstone.lib.nodes.mocks.docker.mysql.docker_mysql_verify import DockerMysqlVerify
from touchstone.lib.nodes.mocks.docker.rabbitmq.docker_rabbitmq import DockerRabbitmq
from touchstone.lib.nodes.mocks.docker.rabbitmq.docker_rabbitmq_context import DockerRabbitmqContext
from touchstone.lib.nodes.mocks.docker.rabbitmq.docker_rabbitmq_setup import DockerRabbitmqSetup
from touchstone.lib.nodes.mocks.docker.rabbitmq.docker_rabbitmq_verify import DockerRabbitmqVerify
from touchstone.lib.nodes.mocks.docker.runnable_docker_mock import RunnableDockerMock
from touchstone.lib.nodes.mocks.docker.s3.docker_s3 import DockerS3
from touchstone.lib.nodes.mocks.docker.s3.docker_s3_setup import DockerS3Setup
from touchstone.lib.nodes.mocks.docker.s3.docker_s3_verify import DockerS3Verify
from touchstone.lib.nodes.mocks.i_mockable import IMockable
from touchstone.lib.nodes.mocks.local.filesystem.local_filesystem import LocalFilesystem
from touchstone.lib.nodes.mocks.local.filesystem.local_filesystem_setup import LocalFilesystemSetup
from touchstone.lib.nodes.mocks.local.filesystem.local_filesystem_verify import LocalFilesystemVerify
from touchstone.lib.nodes.mocks.local.runnable_local_mock import RunnableLocalMock
from touchstone.lib.ts_context import TsContext


class MockFactory(object):
    def __init__(self, ts_context: TsContext, is_dev_mode: bool, root: str, defaults_paths: dict, configs: dict,
                 docker_manager: DockerManager):
        self.__ts_context = ts_context
        self.__is_dev_mode = is_dev_mode
        self.__root = root
        self.__defaults_paths = defaults_paths
        self.__configs = configs
        self.__docker_manager = docker_manager

    def get_mock(self, mock_name: str) -> Optional[IMockable]:
        config = self.__configs.get(mock_name, {})
        mock_defaults_paths = self.__defaults_paths.get(mock_name, None)
        mock = None

        if mock_name == 'http':
            defaults_configurer = FileConfigurer(mock_defaults_paths)
            runnable = DockerHttp(defaults_configurer, HttpHealthCheck(), DockerHttpSetup(), DockerHttpVerify(),
                                  self.__docker_manager, DockerNetwork())
            mock = RunnableDockerMock('http', 'HTTP', runnable)
        elif mock_name == 'rabbitmq':
            defaults_configurer = FileConfigurer(mock_defaults_paths)
            configurer = BasicConfigurer(IRabbitmqBehavior.DEFAULT_CONFIG)
            configurer.merge_config(config)
            context = DockerRabbitmqContext()
            setup = DockerRabbitmqSetup(context)
            verify = DockerRabbitmqVerify(context)
            runnable = DockerRabbitmq(self.__ts_context, defaults_configurer, configurer, HttpHealthCheck(), setup,
                                      verify, self.__docker_manager, DockerNetwork())
            mock = RunnableDockerMock('rabbitmq', 'Rabbit MQ', runnable)
        elif mock_name == 'mongodb':
            defaults_configurer = FileConfigurer(mock_defaults_paths)
            context = DockerMongoContext()
            setup = DockerMongodbSetup(context)
            verify = DockerMongodbVerify(context)
            runnable = DockerMongodb(defaults_configurer, self.__is_dev_mode, setup, verify, self.__docker_manager,
                                     DockerNetwork())
            mock = RunnableDockerMock('mongodb', 'Mongo DB', runnable)
        elif mock_name == 'mysql':
            defaults_configurer = FileConfigurer(mock_defaults_paths)
            configurer = BasicConfigurer(IMysqlBehavior.DEFAULT_CONFIG)
            configurer.merge_config(config)
            context = DockerMysqlContext()
            setup = DockerMysqlSetup(context)
            verify = DockerMysqlVerify(context)
            runnable = DockerMysql(self.__ts_context, defaults_configurer, context, self.__is_dev_mode, configurer,
                                   setup, verify, self.__docker_manager, DockerNetwork())
            mock = RunnableDockerMock('mysql', 'MySQL', runnable)
        elif mock_name == 's3':
            defaults_configurer = FileConfigurer(mock_defaults_paths)
            base_objects_path = os.path.join(self.__root, 'defaults')
            setup = DockerS3Setup()
            verify = DockerS3Verify()
            runnable = DockerS3(defaults_configurer, base_objects_path, HttpHealthCheck(), setup, verify,
                                self.__docker_manager, DockerNetwork())
            mock = RunnableDockerMock('s3', 'S3', runnable)
        elif mock_name == 'filesystem':
            defaults_configurer = FileConfigurer(mock_defaults_paths)
            files_path = os.path.join(self.__root, 'io')
            base_files_path = os.path.join(self.__root, 'defaults', 'filesystem')
            setup = LocalFilesystemSetup(files_path, base_files_path)
            verify = LocalFilesystemVerify(files_path)
            runnable = LocalFilesystem(defaults_configurer, files_path, setup, verify)
            mock = RunnableLocalMock('filesystem', 'Filesystem', runnable)
        return mock
