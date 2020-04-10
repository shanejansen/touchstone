from typing import Optional

import pymysql

from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.mock import Mock
from touchstone.lib.mocks.mock_defaults import MockDefaults
from touchstone.lib.mocks.mysql.mysql_context import MysqlContext
from touchstone.lib.mocks.mysql.mysql_setup import MysqlSetup
from touchstone.lib.mocks.mysql.mysql_verify import MysqlVerify
from touchstone.lib.mocks.network import Network


class Mysql(Mock):
    __USERNAME = 'root'
    __PASSWORD = 'root'

    def __init__(self, host: str, mock_defaults: MockDefaults, is_dev_mode: bool, docker_manager: DockerManager):
        super().__init__(host, mock_defaults)
        self.setup: MysqlSetup = None
        self.verify: MysqlVerify = None
        self.__is_dev_mode = is_dev_mode
        self.__docker_manager = docker_manager
        self.__container_id: Optional[str] = None
        self.__ui_container_id: Optional[str] = None

    @staticmethod
    def name() -> str:
        return 'mysql'

    @staticmethod
    def pretty_name() -> str:
        return 'MySQL'

    def default_config(self) -> dict:
        return {
            'convertCamelToSnakeCase': True
        }

    def run(self) -> Network:
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

        return Network(internal_host=run_result.container_id,
                       internal_port=run_result.internal_port,
                       external_port=run_result.external_port,
                       ui_port=ui_port,
                       username=self.__USERNAME,
                       password=self.__PASSWORD)

    def is_healthy(self) -> bool:
        try:
            pymysql.connect(host=self.network.external_host,
                            port=self.network.external_port,
                            user=self.__USERNAME,
                            password=self.__PASSWORD)
            return True
        except Exception:
            return False

    def initialize(self):
        connection = pymysql.connect(host=self.network.external_host,
                                     port=self.network.external_port,
                                     user=self.__USERNAME,
                                     password=self.__PASSWORD,
                                     charset='utf8mb4',
                                     autocommit=True,
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        mysql_context = MysqlContext()
        convert_camel_to_snake = self.config['convertCamelToSnakeCase']
        self.setup = MysqlSetup(cursor, mysql_context, convert_camel_to_snake)
        self.verify = MysqlVerify(cursor, mysql_context, convert_camel_to_snake)
        self.setup.init(self._mock_defaults.get(self.name()))

    def reset(self):
        self.setup.init(self._mock_defaults.get(self.name()))

    def stop(self):
        if self.__container_id:
            self.__docker_manager.stop_container(self.__container_id)
        if self.__ui_container_id:
            self.__docker_manager.stop_container(self.__ui_container_id)
