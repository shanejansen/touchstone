from typing import List, Tuple

from touchstone.lib import exceptions
from touchstone.lib.health_checks.blocking_health_check import BlockingHealthCheck
from touchstone.lib.nodes.mocks.behaviors.i_filesystem_behavior import IFilesystemBehavior
from touchstone.lib.nodes.mocks.behaviors.i_http_behavior import IHttpBehavior
from touchstone.lib.nodes.mocks.behaviors.i_mongodb_behavior import IMongodbBehavior
from touchstone.lib.nodes.mocks.behaviors.i_mysql_behabior import IMysqlBehavior
from touchstone.lib.nodes.mocks.behaviors.i_rabbitmq_behavior import IRabbitmqBehavior
from touchstone.lib.nodes.mocks.behaviors.i_redis_behavior import IRedisBehavior
from touchstone.lib.nodes.mocks.behaviors.i_s3_behavior import IS3Behavior
from touchstone.lib.nodes.mocks.docker.runnable_docker_mock import RunnableDockerMock
from touchstone.lib.nodes.mocks.i_mockable import IMockable
from touchstone.lib.nodes.mocks.local.runnable_local_mock import RunnableLocalMock


class Mocks(object):
    def __init__(self):
        self.http: IHttpBehavior = None
        self.rabbitmq: IRabbitmqBehavior = None
        self.mongodb: IMongodbBehavior = None
        self.mysql: IMysqlBehavior = None
        self.s3: IS3Behavior = None
        self.filesystem: IFilesystemBehavior = None
        self.redis: IRedisBehavior = None
        self.__runnable_docker_mocks: List[RunnableDockerMock] = []
        self.__runnable_local_mocks: List[RunnableLocalMock] = []
        self.__mocks_running = False

    def register_mock(self, mock: IMockable):
        if isinstance(mock, RunnableLocalMock):
            self.__runnable_local_mocks.append(mock)
        elif isinstance(mock, RunnableDockerMock):
            self.__runnable_docker_mocks.append(mock)
        else:
            raise exceptions.MockException(f'Unsupported mock type: {mock}')

    def start(self):
        if self.__mocks_running:
            print('Mocks have already been started. They cannot be started again.')
        else:
            if self.__runnable_docker_mocks:
                print(f'Starting Docker mocks {[_.get_pretty_name() for _ in self.__runnable_docker_mocks]}...')
                for mock in self.__runnable_docker_mocks:
                    mock.start()
            if self.__runnable_local_mocks:
                print(f'Starting Local mocks {[_.get_pretty_name() for _ in self.__runnable_local_mocks]}...')
                for mock in self.__runnable_local_mocks:
                    mock.start()
            print('Waiting for mocks to become healthy...')
            self.__wait_for_healthy_mocks()
            self.__mocks_running = True
            print('Finished starting mocks.\n')

    def stop(self):
        print('Stopping mocks...')
        for mock in self.__runnable_docker_mocks:
            mock.stop()
        for mock in self.__runnable_local_mocks:
            mock.stop()
        self.__mocks_running = False

    def are_running(self):
        return self.__mocks_running

    def reset(self):
        for mock in self.__runnable_docker_mocks:
            mock.reset()
        for mock in self.__runnable_local_mocks:
            mock.reset()

    def environment_vars(self) -> List[Tuple[str, str]]:
        envs = []
        for mock in self.__runnable_docker_mocks:
            name = mock.get_name().upper()
            envs.append((f'TS_{name}_HOST', mock.get_network().internal_host()))
            envs.append((f'TS_{name}_PORT', mock.get_network().internal_port()))
            envs.append((f'TS_{name}_URL', mock.get_network().internal_url()))
            envs.append((f'TS_{name}_USERNAME', mock.get_network().username()))
            envs.append((f'TS_{name}_PASSWORD', mock.get_network().password()))
        return envs

    def print_available_mocks(self):
        for mock in self.__runnable_docker_mocks:
            message = f'Mock {mock.get_pretty_name()} running with UI: {mock.get_network().ui_url()}'
            if mock.get_network().username():
                message += f' and Username: "{mock.get_network().username()}", ' \
                           f'Password: "{mock.get_network().password()}"'
            print(message)
        for mock in self.__runnable_local_mocks:
            print(f'Mock {mock.get_pretty_name()} running')

    def __wait_for_healthy_mocks(self):
        for mock in self.__runnable_docker_mocks:
            blocking_health_check = BlockingHealthCheck(5, 10, mock)
            is_healthy = blocking_health_check.wait_until_healthy()
            if not is_healthy:
                raise exceptions.MockException(
                    f'Mock {mock.get_pretty_name()} never became healthy and timed out on initialization.')
        for mock in self.__runnable_local_mocks:
            blocking_health_check = BlockingHealthCheck(5, 10, mock)
            is_healthy = blocking_health_check.wait_until_healthy()
            if not is_healthy:
                raise exceptions.MockException(
                    f'Mock {mock.get_pretty_name()} never became healthy and timed out on initialization.')
