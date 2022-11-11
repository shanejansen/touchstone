from touchstone.lib import exceptions
from touchstone.lib.networking.i_network import INetwork
from touchstone.lib.nodes.deps.behaviors.i_behavior import IBehavior
from touchstone.lib.nodes.deps.docker.i_runnable_docker import IRunnableDocker
from touchstone.lib.nodes.deps.i_dependency import IDependency


class RunnableDockerDep(IDependency, IRunnableDocker):
    def __init__(self, name: str, pretty_name: str, runnable_docker: IRunnableDocker):
        self.__name = name
        self.__pretty_name = pretty_name
        self.__runnable_docker = runnable_docker
        self.__has_initialized = False

    def get_name(self) -> str:
        return self.__name

    def get_pretty_name(self) -> str:
        return self.__pretty_name

    def get_behavior(self) -> IBehavior:
        return self.__runnable_docker.get_behavior()

    def initialize(self):
        self.__runnable_docker.initialize()

    def start(self):
        self.__runnable_docker.start()

    def stop(self):
        self.__runnable_docker.stop()

    def reset(self):
        self.__runnable_docker.reset()

    def get_network(self) -> INetwork:
        return self.__runnable_docker.get_network()

    def is_healthy(self) -> bool:
        try:
            self.__runnable_docker.get_network()
        except exceptions.DepException:
            return False
        is_healthy = self.__runnable_docker.is_healthy()
        if is_healthy and not self.__has_initialized:
            self.__runnable_docker.initialize()
            self.__has_initialized = True
        return is_healthy
