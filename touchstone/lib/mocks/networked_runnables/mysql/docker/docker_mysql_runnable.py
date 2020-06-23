import pymysql

from touchstone.lib import exceptions
from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.configurers.i_configurable import IConfigurable
from touchstone.lib.mocks.network import Network
from touchstone.lib.mocks.networked_runnables.i_networked_runnable import INetworkedRunnable
from touchstone.lib.mocks.networked_runnables.mysql.docker.docker_mysql_setup import DockerMysqlSetup
from touchstone.lib.mocks.networked_runnables.mysql.docker.docker_mysql_verify import DockerMysqlVerify
from touchstone.lib.mocks.networked_runnables.mysql.i_mysql_behabior import IMysqlBehavior, IMysqlVerify, IMysqlSetup


class DockerMysqlRunnable(INetworkedRunnable, IMysqlBehavior):
    __USERNAME = 'root'
    __PASSWORD = 'root'

    def __init__(self, defaults_configurer: IConfigurable, is_dev_mode: bool, configurer: IConfigurable,
                 setup: DockerMysqlSetup, verify: DockerMysqlVerify, docker_manager: DockerManager):
        self.__defaults_configurer = defaults_configurer
        self.__is_dev_mode = is_dev_mode
        self.__configurer = configurer
        self.__setup = setup
        self.__verify = verify
        self.__docker_manager = docker_manager
        self.__network = None
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
        convert_camel_to_snake = self.__configurer.get_config()['convertCamelToSnakeCase']
        self.__setup.set_cursor(cursor)
        self.__setup.set_convert_camel_to_snake(convert_camel_to_snake)
        self.__verify.set_cursor(cursor)
        self.__verify.set_convert_camel_to_snake(convert_camel_to_snake)
        self.__setup.init(self.__defaults_configurer.get_config())

    def start(self):
        run_result = self.__docker_manager.run_image(
            'mysql:8.0.20 --default-authentication-plugin=mysql_native_password', port=3306,
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
        self.__setup.init(self.__defaults_configurer.get_config())

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

    def setup(self) -> IMysqlSetup:
        if not self.__setup:
            raise exceptions.MockException('Setup unavailable. Mock is still starting.')
        return self.__setup

    def verify(self) -> IMysqlVerify:
        if not self.__verify:
            raise exceptions.MockException('Verify unavailable. Mock is still starting.')
        return self.__verify
