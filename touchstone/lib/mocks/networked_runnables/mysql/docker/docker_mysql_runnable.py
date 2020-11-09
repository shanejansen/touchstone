import subprocess

import pymysql

from touchstone.lib import exceptions
from touchstone.lib.managers.docker_manager import DockerManager
from touchstone.lib.mocks.configurers.i_configurable import IConfigurable
from touchstone.lib.mocks.networked_runnables.i_networked_runnable import INetworkedRunnable
from touchstone.lib.mocks.networked_runnables.mysql.docker.docker_mysql_context import DockerMysqlContext
from touchstone.lib.mocks.networked_runnables.mysql.docker.docker_mysql_setup import DockerMysqlSetup
from touchstone.lib.mocks.networked_runnables.mysql.docker.docker_mysql_verify import DockerMysqlVerify
from touchstone.lib.mocks.networked_runnables.mysql.i_mysql_behabior import IMysqlBehavior, IMysqlVerify, IMysqlSetup
from touchstone.lib.networking.docker_network import DockerNetwork
from touchstone.lib.networking.i_network import INetwork


class DockerMysqlRunnable(INetworkedRunnable, IMysqlBehavior):
    __USERNAME = 'root'
    __PASSWORD = 'root'

    def __init__(self, defaults_configurer: IConfigurable, mysql_context: DockerMysqlContext, is_dev_mode: bool,
                 configurer: IConfigurable, setup: DockerMysqlSetup, verify: DockerMysqlVerify,
                 docker_manager: DockerManager, docker_network: DockerNetwork):
        self.__defaults_configurer = defaults_configurer
        self.__mysql_context = mysql_context
        self.__is_dev_mode = is_dev_mode
        self.__configurer = configurer
        self.__setup = setup
        self.__verify = verify
        self.__docker_manager = docker_manager
        self.__docker_network = docker_network
        self.__ui_container_id = None

    def get_network(self) -> INetwork:
        return self.__docker_network

    def initialize(self):
        connection = pymysql.connect(host=self.__docker_network.external_host(),
                                     port=self.__docker_network.external_port(),
                                     user=self.__USERNAME,
                                     password=self.__PASSWORD,
                                     charset='utf8mb4',
                                     autocommit=True,
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        convert_camel_to_snake = self.__configurer.get_config()['camel_to_snake']
        self.__setup.set_cursor(cursor)
        self.__setup.set_convert_camel_to_snake(convert_camel_to_snake)
        self.__verify.set_cursor(cursor)
        self.__verify.set_convert_camel_to_snake(convert_camel_to_snake)
        self.__setup.init(self.__defaults_configurer.get_config())

    def start(self):
        run_result = self.__docker_manager.run_background_image(
            'mysql:8.0.20 --default-authentication-plugin=mysql_native_password', port=3306,
            environment_vars=[('MYSQL_ROOT_PASSWORD', self.__USERNAME)])
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
            for database in self.__mysql_context.databases:
                subprocess.run(f'docker exec {self.__docker_network.container_id()} sh -c "mysql -u {self.__USERNAME} '
                               f'-p{self.__PASSWORD} {database} < dump-{database}.sql"', shell=True,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            self.__setup.init(self.__defaults_configurer.get_config())

    def services_available(self):
        if self.__configurer.get_config()['snapshot_databases']:
            for database in self.__mysql_context.databases:
                subprocess.run(
                    f'docker exec {self.__docker_network.container_id()} sh -c "mysqldump -u {self.__USERNAME} '
                    f'-p{self.__PASSWORD} --no-create-db {database} > dump-{database}.sql"', shell=True,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def is_healthy(self) -> bool:
        try:
            pymysql.connect(host=self.__docker_network.external_host(),
                            port=self.__docker_network.external_port(),
                            user=self.__USERNAME,
                            password=self.__PASSWORD)
            return True
        except Exception:
            return False

    def setup(self) -> IMysqlSetup:
        if not self.__setup:
            raise exceptions.MockException('Setup unavailable. Mock is still starting.')
        return self.__setup

    def verify(self) -> IMysqlVerify:
        if not self.__verify:
            raise exceptions.MockException('Verify unavailable. Mock is still starting.')
        return self.__verify
