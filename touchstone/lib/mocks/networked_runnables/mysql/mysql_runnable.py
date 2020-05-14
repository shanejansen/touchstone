import pymysql

from touchstone.lib import exceptions
from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.configurers.BasicConfigurer import BasicConfigurer
from touchstone.lib.mocks.network import Network
from touchstone.lib.mocks.networked_runnables.i_networked_runnable import INetworkedRunnable
from touchstone.lib.mocks.networked_runnables.mysql.i_mysql_behabior import IMysqlBehavior
from touchstone.lib.mocks.networked_runnables.mysql.mysql_context import MysqlContext
from touchstone.lib.mocks.networked_runnables.mysql.mysql_setup import MysqlSetup
from touchstone.lib.mocks.networked_runnables.mysql.mysql_verify import MysqlVerify


class MysqlRunnable(INetworkedRunnable, IMysqlBehavior):
    __USERNAME = 'root'
    __PASSWORD = 'root'
    __DEFAULT_CONFIG = {
        'convertCamelToSnakeCase': True
    }

    def __init__(self, is_dev_mode: bool, defaults: dict, config: dict, docker_manager: DockerManager):
        self.__is_dev_mode = is_dev_mode
        self.__defaults = defaults
        self.__config = BasicConfigurer(self.__DEFAULT_CONFIG)
        self.__config.merge_config(config)
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
        connection = pymysql.connect(host=self.get_network().external_host,
                                     port=self.get_network().external_port,
                                     user=self.__USERNAME,
                                     password=self.__PASSWORD,
                                     charset='utf8mb4',
                                     autocommit=True,
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        mysql_context = MysqlContext()
        convert_camel_to_snake = self.__config.get_config()['convertCamelToSnakeCase']
        self.__setup = MysqlSetup(cursor, mysql_context, convert_camel_to_snake)
        self.__verify = MysqlVerify(cursor, mysql_context, convert_camel_to_snake)
        self.__setup.init(self.__defaults)

    def start(self):
        run_result = self.__docker_manager.run_image('mysql:5.7.29', port=3306,
                                                     environment_vars=[('MYSQL_ROOT_PASSWORD', self.__USERNAME)])
        self.__container_id = run_result.container_id

        ui_port = None
        if self.__is_dev_mode:
            ui_run_result = self.__docker_manager.run_image('adminer:4.7.5-standalone',
                                                            ui_port=8080,
                                                            environment_vars=[
                                                                ('ADMINER_DEFAULT_SERVER', self.__container_id)])
            self.__ui_container_id = ui_run_result.container_id
            ui_port = ui_run_result.ui_port

        self.__network = Network(internal_host=run_result.container_id,
                                 internal_port=run_result.internal_port,
                                 external_port=run_result.external_port,
                                 ui_port=ui_port,
                                 username=self.__USERNAME,
                                 password=self.__PASSWORD)

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
            pymysql.connect(host=self.get_network().external_host,
                            port=self.get_network().external_port,
                            user=self.__USERNAME,
                            password=self.__PASSWORD)
            return True
        except Exception:
            return False

    def setup(self) -> MysqlSetup:
        if not self.__setup:
            raise exceptions.MockException('Setup unavailable. Mock is still starting.')
        return self.__setup

    def verify(self) -> MysqlVerify:
        if not self.__verify:
            raise exceptions.MockException('Verify unavailable. Mock is still starting.')
        return self.__verify
