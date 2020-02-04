from typing import Optional

import pymysql

from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.mock import Mock
from touchstone.lib.mocks.mysql.mysql_context import MysqlContext
from touchstone.lib.mocks.mysql.mysql_setup import MysqlSetup
from touchstone.lib.mocks.mysql.mysql_verify import MysqlVerify
from touchstone.lib.mocks.network import Network


class Mysql(Mock):
    def __init__(self, host: str, is_dev_mode: bool, docker_manager: DockerManager):
        super().__init__(host)
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
                                                     environment_vars=[('MYSQL_ROOT_PASSWORD', 'root')])
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
                       ui_port=ui_port)

    def is_healthy(self) -> bool:
        try:
            pymysql.connect(host=self.network.external_host,
                            port=self.network.external_port,
                            user='root',
                            password='root')
            return True
        except Exception:
            return False

    def initialize(self):
        connection = pymysql.connect(host=self.network.external_host,
                                     port=self.network.external_port,
                                     user='root',
                                     password='root',
                                     charset='utf8mb4',
                                     autocommit=True,
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        mysql_context = MysqlContext()
        convert_camel_to_snake = self.config['convertCamelToSnakeCase']
        self.setup = MysqlSetup(cursor, mysql_context, convert_camel_to_snake)
        self.verify = MysqlVerify(cursor, mysql_context, convert_camel_to_snake)

    def load_defaults(self, defaults: dict):
        self.setup.load_defaults(defaults)

    def stop(self):
        if self.__container_id:
            self.__docker_manager.stop_container(self.__container_id)
        if self.__ui_container_id:
            self.__docker_manager.stop_container(self.__ui_container_id)
