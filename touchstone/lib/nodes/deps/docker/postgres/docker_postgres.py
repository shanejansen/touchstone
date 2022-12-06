import subprocess

import psycopg2

from touchstone.lib import exceptions
from touchstone.lib.configurers.i_configurable import IConfigurable
from touchstone.lib.listeners.i_services_available_listener import IServicesAvailableListener
from touchstone.lib.managers.docker_manager import DockerManager
from touchstone.lib.networking.docker_network import DockerNetwork
from touchstone.lib.networking.i_network import INetwork
from touchstone.lib.nodes.deps.behaviors.i_behavior import IBehavior
from touchstone.lib.nodes.deps.behaviors.i_database_behabior import IDatabaseBehavior, IDatabaseVerify, IDatabaseSetup
from touchstone.lib.nodes.deps.docker.i_runnable_docker import IRunnableDocker
from touchstone.lib.nodes.deps.docker.postgres.docker_postgres_context import DockerPostgresContext
from touchstone.lib.nodes.deps.docker.postgres.docker_postgres_setup import DockerPostgresSetup
from touchstone.lib.nodes.deps.docker.postgres.docker_postgres_verify import DockerPostgresVerify
from touchstone.lib.ts_context import TsContext


class DockerPostgres(IRunnableDocker, IDatabaseBehavior, IServicesAvailableListener):
    __USERNAME = 'root'
    __PASSWORD = 'root'

    def __init__(self, ts_context: TsContext, defaults_configurer: IConfigurable,
                 postgres_context: DockerPostgresContext, is_dev_mode: bool, configurer: IConfigurable,
                 setup: DockerPostgresSetup, verify: DockerPostgresVerify, docker_manager: DockerManager,
                 docker_network: DockerNetwork):
        ts_context.register_services_available_listener(self)
        self.__defaults_configurer = defaults_configurer
        self.__postgres_context = postgres_context
        self.__is_dev_mode = is_dev_mode
        self.__configurer = configurer
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
        connection = psycopg2.connect(host=self.__docker_network.external_host(),
                                      port=self.__docker_network.external_port(),
                                      user=self.__USERNAME,
                                      password=self.__PASSWORD)
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        convert_camel_to_snake = self.__configurer.get_config()['camel_to_snake']
        self.__setup.set_cursor(cursor)
        self.__setup.set_convert_camel_to_snake(convert_camel_to_snake)
        self.__verify.set_cursor(cursor)
        self.__verify.set_convert_camel_to_snake(convert_camel_to_snake)
        self.__setup.init(self.__defaults_configurer.get_config())

    def start(self):
        run_result = self.__docker_manager.run_background_image(
            'postgres:14.4-alpine', port=5432,
            environment_vars=[('POSTGRES_USER', self.__USERNAME), ('POSTGRES_PASSWORD', self.__PASSWORD)])
        self.__docker_network.set_container_id(run_result.container_id)
        if self.__is_dev_mode:
            ui_run_result = self.__docker_manager.run_background_image('adminer:4.7.5-standalone',
                                                                       ui_port=8080,
                                                                       environment_vars=[
                                                                           ('ADMINER_DEFAULT_SERVER',
                                                                            self.__docker_network.internal_host())])
            self.__ui_container_id = ui_run_result.container_id
            self.__docker_network.set_ui_port(ui_run_result.ui_port)
        self.__docker_network.set_internal_port(run_result.internal_port)
        self.__docker_network.set_external_port(run_result.external_port)
        self.__docker_network.set_username(self.__USERNAME)
        self.__docker_network.set_password(self.__PASSWORD)

    def stop(self):
        if self.__docker_network.container_id():
            self.__docker_manager.stop_container(self.__docker_network.container_id())
        if self.__ui_container_id:
            self.__docker_manager.stop_container(self.__ui_container_id)

    def reset(self):
        if self.__configurer.get_config()['snapshot_databases']:
            self.__setup.recreate_databases()
            subprocess.run(f'docker exec {self.__docker_network.container_id()} sh -c "psql {self.__USERNAME} '
                           f'< dump-{self.__USERNAME}.bak"', shell=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            self.__setup.init(self.__defaults_configurer.get_config())

    def is_healthy(self) -> bool:
        try:
            psycopg2.connect(host=self.__docker_network.external_host(),
                             port=self.__docker_network.external_port(),
                             user=self.__USERNAME,
                             password=self.__PASSWORD)
            return True
        except Exception:
            return False

    def setup(self) -> IDatabaseSetup:
        if not self.__setup:
            raise exceptions.DepException('Setup unavailable. Dependency is still starting.')
        return self.__setup

    def verify(self) -> IDatabaseVerify:
        if not self.__verify:
            raise exceptions.DepException('Verify unavailable. Dependency is still starting.')
        return self.__verify

    def services_available(self):
        if self.__configurer.get_config()['snapshot_databases']:
            subprocess.run(
                f'docker exec {self.__docker_network.container_id()} sh -c "pg_dump {self.__USERNAME} '
                f'> dump-{self.__USERNAME}.bak"', shell=True,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
