from typing import List, Tuple

from touchstone.lib import exceptions
from touchstone.lib.health_checks.blocking_health_check import BlockingHealthCheck
from touchstone.lib.nodes.deps.behaviors.i_database_behabior import IDatabaseBehavior
from touchstone.lib.nodes.deps.behaviors.i_filesystem_behavior import IFilesystemBehavior
from touchstone.lib.nodes.deps.behaviors.i_http_behavior import IHttpBehavior
from touchstone.lib.nodes.deps.behaviors.i_mongodb_behavior import IMongodbBehavior
from touchstone.lib.nodes.deps.behaviors.i_rabbitmq_behavior import IRabbitmqBehavior
from touchstone.lib.nodes.deps.behaviors.i_redis_behavior import IRedisBehavior
from touchstone.lib.nodes.deps.behaviors.i_s3_behavior import IS3Behavior
from touchstone.lib.nodes.deps.docker.runnable_docker_dep import RunnableDockerDep
from touchstone.lib.nodes.deps.i_dependency import IDependency
from touchstone.lib.nodes.deps.local.runnable_local_dep import RunnableLocalDep


class Deps(object):
    def __init__(self):
        self.http: IHttpBehavior = None
        self.rabbitmq: IRabbitmqBehavior = None
        self.mongodb: IMongodbBehavior = None
        self.mysql: IDatabaseBehavior = None
        self.postgres: IDatabaseBehavior = None
        self.s3: IS3Behavior = None
        self.filesystem: IFilesystemBehavior = None
        self.redis: IRedisBehavior = None
        self.__runnable_docker_deps: List[RunnableDockerDep] = []
        self.__runnable_local_deps: List[RunnableLocalDep] = []
        self.__deps_running = False

    def register_dep(self, dep: IDependency):
        if isinstance(dep, RunnableLocalDep):
            self.__runnable_local_deps.append(dep)
        elif isinstance(dep, RunnableDockerDep):
            self.__runnable_docker_deps.append(dep)
        else:
            raise exceptions.DepException(f'Unsupported dependency type: {dep}')

    def start(self):
        if self.__deps_running:
            print('Dependencies have already been started. They cannot be started again.')
        else:
            if self.__runnable_docker_deps:
                print(f'Starting Docker dependencies {[_.get_pretty_name() for _ in self.__runnable_docker_deps]}...')
                for dep in self.__runnable_docker_deps:
                    dep.start()
            if self.__runnable_local_deps:
                print(f'Starting Local dependencies {[_.get_pretty_name() for _ in self.__runnable_local_deps]}...')
                for dep in self.__runnable_local_deps:
                    dep.start()
            print('Waiting for dependencies to become healthy...')
            self.__wait_for_healthy_deps()
            self.__deps_running = True
            print('Finished starting dependencies.\n')

    def stop(self):
        print('Stopping dependencies...')
        for dep in self.__runnable_docker_deps:
            dep.stop()
        for dep in self.__runnable_local_deps:
            dep.stop()
        self.__deps_running = False

    def are_running(self):
        return self.__deps_running

    def reset(self):
        for dep in self.__runnable_docker_deps:
            dep.reset()
        for dep in self.__runnable_local_deps:
            dep.reset()

    def environment_vars(self) -> List[Tuple[str, str]]:
        envs = []
        for dep in self.__runnable_docker_deps:
            name = dep.get_name().upper()
            envs.append((f'TS_{name}_HOST', dep.get_network().internal_host()))
            envs.append((f'TS_{name}_PORT', dep.get_network().internal_port()))
            envs.append((f'TS_{name}_URL', dep.get_network().internal_url()))
            envs.append((f'TS_{name}_USERNAME', dep.get_network().username()))
            envs.append((f'TS_{name}_PASSWORD', dep.get_network().password()))
        return envs

    def print_available_deps(self):
        for dep in self.__runnable_docker_deps:
            message = f'Dependency {dep.get_pretty_name()} running with UI: {dep.get_network().ui_url()}'
            if dep.get_network().username():
                message += f' and Username: "{dep.get_network().username()}", ' \
                           f'Password: "{dep.get_network().password()}"'
            print(message)
        for dep in self.__runnable_local_deps:
            print(f'Dependency {dep.get_pretty_name()} running')

    def __wait_for_healthy_deps(self):
        for dep in self.__runnable_docker_deps:
            blocking_health_check = BlockingHealthCheck(5, 10, dep)
            is_healthy = blocking_health_check.wait_until_healthy()
            if not is_healthy:
                raise exceptions.DepException(
                    f'Dependency {dep.get_pretty_name()} never became healthy and timed out on initialization.')
        for dep in self.__runnable_local_deps:
            blocking_health_check = BlockingHealthCheck(5, 10, dep)
            is_healthy = blocking_health_check.wait_until_healthy()
            if not is_healthy:
                raise exceptions.DepException(
                    f'Dependency {dep.get_pretty_name()} never became healthy and timed out on initialization.')
