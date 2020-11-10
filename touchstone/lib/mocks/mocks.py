from typing import List, Tuple

from touchstone.lib import exceptions
from touchstone.lib.health_checks.blocking_health_check import BlockingHealthCheck
from touchstone.lib.health_checks.i_health_checkable import IHealthCheckable
from touchstone.lib.mocks.mockables.i_mockable import IMockable
from touchstone.lib.mocks.mockables.networked_mock import NetworkedMock
from touchstone.lib.mocks.networked_runnables.http.i_http_behavior import IHttpBehavior
from touchstone.lib.mocks.networked_runnables.mongodb.i_mongodb_behavior import IMongodbBehavior
from touchstone.lib.mocks.networked_runnables.mysql.i_mysql_behabior import IMysqlBehavior
from touchstone.lib.mocks.networked_runnables.rabbitmq.i_rabbitmq_behavior import IRabbitmqBehavior
from touchstone.lib.mocks.networked_runnables.s3.i_s3_behavior import IS3Behavior
from touchstone.lib.mocks.runnables.filesystem.i_filesystem_behavior import IFilesystemBehavior


class Mocks(object):
    def __init__(self):
        self.http: IHttpBehavior = None
        self.rabbitmq: IRabbitmqBehavior = None
        self.mongodb: IMongodbBehavior = None
        self.mysql: IMysqlBehavior = None
        self.s3: IS3Behavior = None
        self.filesystem: IFilesystemBehavior = None
        self.__registered_mocks: List[IMockable] = []
        self.__mocks_running = False

    def register_mock(self, mock: IMockable):
        self.__registered_mocks.append(mock)

    def start(self):
        if self.__mocks_running:
            print('Mocks have already been started. They cannot be started again.')
        else:
            print(f'Starting mocks {[_.get_pretty_name() for _ in self.__registered_mocks]}...')
            for mock in self.__registered_mocks:
                mock.start()
            self.__wait_for_healthy_mocks()
            self.__mocks_running = True
            print('Finished starting mocks.\n')

    def stop(self):
        print('Stopping mocks...')
        for mock in self.__registered_mocks:
            mock.stop()
        self.__mocks_running = False

    def are_running(self):
        return self.__mocks_running

    def services_became_available(self):
        for mock in self.__registered_mocks:
            mock.services_available()

    def reset(self):
        for mock in self.__registered_mocks:
            mock.reset()

    def environment_vars(self) -> List[Tuple[str, str]]:
        envs = []
        for mock in self.__registered_mocks:
            if isinstance(mock, NetworkedMock):
                name = mock.get_name().upper()
                envs.append((f'TS_{name}_HOST', mock.get_network().internal_host()))
                envs.append((f'TS_{name}_PORT', mock.get_network().internal_port()))
                envs.append((f'TS_{name}_URL', mock.get_network().internal_url()))
                envs.append((f'TS_{name}_USERNAME', mock.get_network().username()))
                envs.append((f'TS_{name}_PASSWORD', mock.get_network().password()))
        return envs

    def print_available_mocks(self):
        for mock in self.__registered_mocks:
            message = f'Mock {mock.get_pretty_name()} running'
            if isinstance(mock, NetworkedMock):
                message += f' with UI: {mock.get_network().ui_url()}'
                if mock.get_network().username():
                    message += f' and Username: "{mock.get_network().username()}", ' \
                               f'Password: "{mock.get_network().password()}"'
            print(message)

    def __wait_for_healthy_mocks(self):
        for mock in self.__registered_mocks:
            health_checkable = mock
            if isinstance(health_checkable, IHealthCheckable):
                blocking_health_check = BlockingHealthCheck(5, 10, health_checkable)
                is_healthy = blocking_health_check.wait_until_healthy()
                if not is_healthy:
                    raise exceptions.MockException(
                        f'Mock {mock.get_pretty_name()} never became healthy and timed out on initialization.')
