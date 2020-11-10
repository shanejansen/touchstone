from touchstone.lib import exceptions
from touchstone.lib.health_checks.http_health_check import HttpHealthCheck
from touchstone.lib.managers.docker_manager import DockerManager
from touchstone.lib.mocks.configurers.i_configurable import IConfigurable
from touchstone.lib.mocks.networked_runnables.http.docker.docker_http_setup import DockerHttpSetup
from touchstone.lib.mocks.networked_runnables.http.docker.docker_http_verify import DockerHttpVerify
from touchstone.lib.mocks.networked_runnables.http.i_http_behavior import IHttpBehavior, IHttpSetup, IHttpVerify
from touchstone.lib.mocks.networked_runnables.i_networked_runnable import INetworkedRunnable
from touchstone.lib.networking.docker_network import DockerNetwork
from touchstone.lib.networking.i_network import INetwork


class DockerHttpRunnable(INetworkedRunnable, IHttpBehavior):
    def __init__(self, defaults_configurer: IConfigurable, health_check: HttpHealthCheck, setup: DockerHttpSetup,
                 verify: DockerHttpVerify, docker_manager: DockerManager, docker_network: DockerNetwork):
        self.__defaults_configurer = defaults_configurer
        self.__health_check = health_check
        self.__setup = setup
        self.__verify = verify
        self.__docker_manager = docker_manager
        self.__docker_network = docker_network

    def get_network(self) -> INetwork:
        return self.__docker_network

    def initialize(self):
        self.__setup.set_url(self.__docker_network.external_url())
        self.__verify.set_url(self.__docker_network.external_url())
        self.__setup.init(self.__defaults_configurer.get_config())

    def start(self):
        run_result = self.__docker_manager.run_background_image('holomekc/wiremock-gui:2.25.1', port=8080,
                                                                exposed_port=9090)
        self.__docker_network.set_container_id(run_result.container_id)
        self.__docker_network.set_internal_port(run_result.internal_port)
        self.__docker_network.set_external_port(run_result.external_port)
        self.__docker_network.set_ui_port(run_result.external_port)
        self.__docker_network.set_ui_endpoint('/__admin/webapp')
        self.__docker_network.set_prefix('http://')

    def stop(self):
        if self.__docker_network.container_id():
            self.__docker_manager.stop_container(self.__docker_network.container_id())

    def reset(self):
        self.__setup.init(self.__defaults_configurer.get_config())

    def services_available(self):
        pass

    def is_healthy(self) -> bool:
        self.__health_check.set_url(self.__docker_network.ui_url())
        return self.__health_check.is_healthy()

    def setup(self) -> IHttpSetup:
        if not self.__setup:
            raise exceptions.MockException('Setup unavailable. Mock is still starting.')
        return self.__setup

    def verify(self) -> IHttpVerify:
        if not self.__verify:
            raise exceptions.MockException('Verify unavailable. Mock is still starting.')
        return self.__verify

    def url(self) -> str:
        return self.__docker_network.external_url()
