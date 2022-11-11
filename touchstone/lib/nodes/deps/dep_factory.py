import os
from typing import Optional

from touchstone.lib.configurers.BasicConfigurer import BasicConfigurer
from touchstone.lib.configurers.FileConfigurer import FileConfigurer
from touchstone.lib.health_checks.http_health_check import HttpHealthCheck
from touchstone.lib.managers.docker_manager import DockerManager
from touchstone.lib.networking.docker_network import DockerNetwork
from touchstone.lib.nodes.deps.behaviors.i_database_behabior import IDatabaseBehavior
from touchstone.lib.nodes.deps.behaviors.i_rabbitmq_behavior import IRabbitmqBehavior
from touchstone.lib.nodes.deps.docker.http.docker_http import DockerHttp
from touchstone.lib.nodes.deps.docker.http.docker_http_setup import DockerHttpSetup
from touchstone.lib.nodes.deps.docker.http.docker_http_verify import DockerHttpVerify
from touchstone.lib.nodes.deps.docker.mongodb.docker_mongo_context import DockerMongoContext
from touchstone.lib.nodes.deps.docker.mongodb.docker_mongodb import DockerMongodb
from touchstone.lib.nodes.deps.docker.mongodb.docker_mongodb_setup import DockerMongodbSetup
from touchstone.lib.nodes.deps.docker.mongodb.docker_mongodb_verify import DockerMongodbVerify
from touchstone.lib.nodes.deps.docker.mysql.docker_mysql import DockerMysql
from touchstone.lib.nodes.deps.docker.mysql.docker_mysql_context import DockerMysqlContext
from touchstone.lib.nodes.deps.docker.mysql.docker_mysql_setup import DockerMysqlSetup
from touchstone.lib.nodes.deps.docker.mysql.docker_mysql_verify import DockerMysqlVerify
from touchstone.lib.nodes.deps.docker.postgres.docker_postgres import DockerPostgres
from touchstone.lib.nodes.deps.docker.postgres.docker_postgres_context import DockerPostgresContext
from touchstone.lib.nodes.deps.docker.postgres.docker_postgres_setup import DockerPostgresSetup
from touchstone.lib.nodes.deps.docker.postgres.docker_postgres_verify import DockerPostgresVerify
from touchstone.lib.nodes.deps.docker.rabbitmq.docker_rabbitmq import DockerRabbitmq
from touchstone.lib.nodes.deps.docker.rabbitmq.docker_rabbitmq_context import DockerRabbitmqContext
from touchstone.lib.nodes.deps.docker.rabbitmq.docker_rabbitmq_setup import DockerRabbitmqSetup
from touchstone.lib.nodes.deps.docker.rabbitmq.docker_rabbitmq_verify import DockerRabbitmqVerify
from touchstone.lib.nodes.deps.docker.redis.docker_redis import DockerRedis
from touchstone.lib.nodes.deps.docker.redis.docker_redis_setup import DockerRedisSetup
from touchstone.lib.nodes.deps.docker.redis.docker_redis_verify import DockerRedisVerify
from touchstone.lib.nodes.deps.docker.runnable_docker_dep import RunnableDockerDep
from touchstone.lib.nodes.deps.docker.s3.docker_s3 import DockerS3
from touchstone.lib.nodes.deps.docker.s3.docker_s3_setup import DockerS3Setup
from touchstone.lib.nodes.deps.docker.s3.docker_s3_verify import DockerS3Verify
from touchstone.lib.nodes.deps.i_dependency import IDependency
from touchstone.lib.nodes.deps.local.filesystem.local_filesystem import LocalFilesystem
from touchstone.lib.nodes.deps.local.filesystem.local_filesystem_setup import LocalFilesystemSetup
from touchstone.lib.nodes.deps.local.filesystem.local_filesystem_verify import LocalFilesystemVerify
from touchstone.lib.nodes.deps.local.runnable_local_dep import RunnableLocalDep
from touchstone.lib.ts_context import TsContext


class DepFactory(object):
    def __init__(self, ts_context: TsContext, is_dev_mode: bool, root: str, defaults_paths: dict, configs: dict,
                 docker_manager: DockerManager):
        self.__ts_context = ts_context
        self.__is_dev_mode = is_dev_mode
        self.__root = root
        self.__defaults_paths = defaults_paths
        self.__configs = configs
        self.__docker_manager = docker_manager

    def get_dep(self, dep_name: str) -> Optional[IDependency]:
        config = self.__configs.get(dep_name, {})
        dep_defaults_paths = self.__defaults_paths.get(dep_name, None)
        dep = None

        if dep_name == 'http':
            defaults_configurer = FileConfigurer(dep_defaults_paths)
            runnable = DockerHttp(defaults_configurer, HttpHealthCheck(), DockerHttpSetup(), DockerHttpVerify(),
                                  self.__docker_manager, DockerNetwork())
            dep = RunnableDockerDep('http', 'HTTP', runnable)
        elif dep_name == 'rabbitmq':
            defaults_configurer = FileConfigurer(dep_defaults_paths)
            configurer = BasicConfigurer(IRabbitmqBehavior.DEFAULT_CONFIG)
            configurer.merge_config(config)
            context = DockerRabbitmqContext()
            setup = DockerRabbitmqSetup(context)
            verify = DockerRabbitmqVerify(context)
            runnable = DockerRabbitmq(self.__ts_context, defaults_configurer, configurer, HttpHealthCheck(), setup,
                                      verify, self.__docker_manager, DockerNetwork())
            dep = RunnableDockerDep('rabbitmq', 'Rabbit MQ', runnable)
        elif dep_name == 'mongodb':
            defaults_configurer = FileConfigurer(dep_defaults_paths)
            context = DockerMongoContext()
            setup = DockerMongodbSetup(context)
            verify = DockerMongodbVerify(context)
            runnable = DockerMongodb(defaults_configurer, self.__is_dev_mode, setup, verify, self.__docker_manager,
                                     DockerNetwork())
            dep = RunnableDockerDep('mongodb', 'Mongo DB', runnable)
        elif dep_name == 'mysql':
            defaults_configurer = FileConfigurer(dep_defaults_paths)
            configurer = BasicConfigurer(IDatabaseBehavior.DEFAULT_CONFIG)
            configurer.merge_config(config)
            context = DockerMysqlContext()
            setup = DockerMysqlSetup(context)
            verify = DockerMysqlVerify(context)
            runnable = DockerMysql(self.__ts_context, defaults_configurer, context, self.__is_dev_mode, configurer,
                                   setup, verify, self.__docker_manager, DockerNetwork())
            dep = RunnableDockerDep('mysql', 'MySQL', runnable)
        elif dep_name == 'postgres':
            defaults_configurer = FileConfigurer(dep_defaults_paths)
            configurer = BasicConfigurer(IDatabaseBehavior.DEFAULT_CONFIG)
            configurer.merge_config(config)
            context = DockerPostgresContext()
            setup = DockerPostgresSetup(context)
            verify = DockerPostgresVerify(context)
            runnable = DockerPostgres(self.__ts_context, defaults_configurer, context, self.__is_dev_mode, configurer,
                                      setup, verify, self.__docker_manager, DockerNetwork())
            dep = RunnableDockerDep('postgres', 'PostgreSQL', runnable)
        elif dep_name == 's3':
            defaults_configurer = FileConfigurer(dep_defaults_paths)
            base_objects_path = os.path.join(self.__root, 'defaults')
            setup = DockerS3Setup()
            verify = DockerS3Verify()
            runnable = DockerS3(defaults_configurer, base_objects_path, HttpHealthCheck(), setup, verify,
                                self.__docker_manager, DockerNetwork())
            dep = RunnableDockerDep('s3', 'S3', runnable)
        elif dep_name == 'filesystem':
            defaults_configurer = FileConfigurer(dep_defaults_paths)
            files_path = os.path.join(self.__root, 'io')
            base_files_path = os.path.join(self.__root, 'defaults', 'filesystem')
            setup = LocalFilesystemSetup(files_path, base_files_path)
            verify = LocalFilesystemVerify(files_path)
            runnable = LocalFilesystem(defaults_configurer, files_path, setup, verify)
            dep = RunnableLocalDep('filesystem', 'Filesystem', runnable)
        elif dep_name == 'redis':
            defaults_configurer = FileConfigurer(dep_defaults_paths)
            setup = DockerRedisSetup()
            verify = DockerRedisVerify()
            runnable = DockerRedis(defaults_configurer, self.__is_dev_mode, setup, verify, self.__docker_manager,
                                   DockerNetwork())
            dep = RunnableDockerDep('redis', 'Redis', runnable)
        return dep
