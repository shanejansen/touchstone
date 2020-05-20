import os
from typing import Optional

from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.configurers.BasicConfigurer import BasicConfigurer
from touchstone.lib.mocks.health_checks.http_health_check import HttpHealthCheck
from touchstone.lib.mocks.mockables.basic_mock import BasicMock
from touchstone.lib.mocks.mockables.i_mockable import IMockable
from touchstone.lib.mocks.mockables.networked_mock import NetworkedMock
from touchstone.lib.mocks.networked_runnables.http.docker.docker_http_runnable import DockerHttpRunnable
from touchstone.lib.mocks.networked_runnables.http.docker.docker_http_setup import DockerHttpSetup
from touchstone.lib.mocks.networked_runnables.http.docker.docker_http_verify import DockerHttpVerify
from touchstone.lib.mocks.networked_runnables.mongodb.docker.docker_mongo_context import DockerMongoContext
from touchstone.lib.mocks.networked_runnables.mongodb.docker.docker_mongodb_runnable import DockerMongodbRunnable
from touchstone.lib.mocks.networked_runnables.mongodb.docker.docker_mongodb_setup import DockerMongodbSetup
from touchstone.lib.mocks.networked_runnables.mongodb.docker.docker_mongodb_verify import DockerMongodbVerify
from touchstone.lib.mocks.networked_runnables.mysql.docker.docker_mysql_context import DockerMysqlContext
from touchstone.lib.mocks.networked_runnables.mysql.docker.docker_mysql_runnable import DockerMysqlRunnable
from touchstone.lib.mocks.networked_runnables.mysql.docker.docker_mysql_setup import DockerMysqlSetup
from touchstone.lib.mocks.networked_runnables.mysql.docker.docker_mysql_verify import DockerMysqlVerify
from touchstone.lib.mocks.networked_runnables.mysql.i_mysql_behabior import IMysqlBehavior
from touchstone.lib.mocks.networked_runnables.rabbitmq.docker.docker_rabbitmq_context import DockerRabbitmqContext
from touchstone.lib.mocks.networked_runnables.rabbitmq.docker.docker_rabbitmq_runnable import DockerRabbitmqRunnable
from touchstone.lib.mocks.networked_runnables.rabbitmq.docker.docker_rabbitmq_setup import DockerRabbitmqSetup
from touchstone.lib.mocks.networked_runnables.rabbitmq.docker.docker_rabbitmq_verify import DockerRabbitmqVerify
from touchstone.lib.mocks.networked_runnables.rabbitmq.i_rabbitmq_behavior import IRabbitmqBehavior
from touchstone.lib.mocks.networked_runnables.s3.docker.docker_s3_runnable import DockerS3Runnable
from touchstone.lib.mocks.networked_runnables.s3.docker.docker_s3_setup import DockerS3Setup
from touchstone.lib.mocks.networked_runnables.s3.docker.docker_s3_verify import DockerS3Verify
from touchstone.lib.mocks.runnables.filesystem.local.local_filesystem_runnable import LocalFilesystemRunnable
from touchstone.lib.mocks.runnables.filesystem.local.local_filesystem_setup import LocalFilesystemSetup
from touchstone.lib.mocks.runnables.filesystem.local.local_filesystem_verify import LocalFilesystemVerify


class MockFactory(object):
    def __init__(self, is_dev_mode: bool, root: str, defaults: dict, configs: dict, host: str,
                 docker_manager: DockerManager):
        self.__is_dev_mode = is_dev_mode
        self.__root = root
        self.__defaults = defaults
        self.__configs = configs
        self.__host = host
        self.__docker_manager = docker_manager

    def get_mock(self, mock_name: str) -> Optional[IMockable]:
        config = self.__configs.get(mock_name, {})
        mock_defaults = self.__defaults.get(mock_name, {})
        mock = None

        if mock_name == 'http':
            runnable = DockerHttpRunnable(mock_defaults, HttpHealthCheck(), DockerHttpSetup(), DockerHttpVerify(),
                                          self.__docker_manager)
            mock = NetworkedMock('http', 'HTTP', self.__host, runnable)
        elif mock_name == 'rabbitmq':
            configurer = BasicConfigurer(IRabbitmqBehavior.DEFAULT_CONFIG)
            configurer.merge_config(config)
            context = DockerRabbitmqContext()
            setup = DockerRabbitmqSetup(context)
            verify = DockerRabbitmqVerify(context)
            runnable = DockerRabbitmqRunnable(mock_defaults, configurer, HttpHealthCheck(), setup, verify,
                                              self.__docker_manager)
            mock = NetworkedMock('rabbitmq', 'Rabbit MQ', self.__host, runnable)
        elif mock_name == 'mongodb':
            context = DockerMongoContext()
            setup = DockerMongodbSetup(context)
            verify = DockerMongodbVerify(context)
            runnable = DockerMongodbRunnable(mock_defaults, self.__is_dev_mode, setup, verify, self.__docker_manager)
            mock = NetworkedMock('mongodb', 'Mongo DB', self.__host, runnable)
        elif mock_name == 'mysql':
            configurer = BasicConfigurer(IMysqlBehavior.DEFAULT_CONFIG)
            configurer.merge_config(config)
            context = DockerMysqlContext()
            setup = DockerMysqlSetup(context)
            verify = DockerMysqlVerify(context)
            runnable = DockerMysqlRunnable(self.__is_dev_mode, mock_defaults, configurer, setup, verify,
                                           self.__docker_manager)
            mock = NetworkedMock('mysql', 'MySQL', self.__host, runnable)
        elif mock_name == 's3':
            base_objects_path = os.path.join(self.__root, 'defaults')
            setup = DockerS3Setup()
            verify = DockerS3Verify()
            runnable = DockerS3Runnable(mock_defaults, base_objects_path, HttpHealthCheck(), setup, verify,
                                        self.__docker_manager)
            mock = NetworkedMock('s3', 'S3', self.__host, runnable)
        elif mock_name == 'filesystem':
            base_files_path = os.path.join(self.__root, 'defaults')
            setup = LocalFilesystemSetup(base_files_path)
            verify = LocalFilesystemVerify(base_files_path)
            runnable = LocalFilesystemRunnable(mock_defaults, base_files_path, setup, verify)
            mock = BasicMock('filesystem', 'Filesystem', runnable)
        return mock
