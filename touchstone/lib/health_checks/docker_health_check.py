import subprocess
import urllib.error
import urllib.request

from touchstone import common
from touchstone.lib import exceptions
from touchstone.lib.health_checks.i_health_checkable import IHealthCheckable


class DockerHealthCheck(IHealthCheckable):
    def __init__(self):
        self.__container_id = None

    def set_container_id(self, container_id: str):
        self.__container_id = container_id

    def is_healthy(self) -> bool:
        if not self.__container_id:
            raise exceptions.MockException('Container ID must be set before checking health.')
        try:
            common.logger.debug(f'Executing Docker health check for container ID: {self.__container_id}')
            passed = 'healthy' in str(
                subprocess.run(['docker', 'inspect', "--format='{{.State.Health.Status}}'", self.__container_id],
                               stdout=subprocess.PIPE).stdout, encoding='utf-8')
            if passed:
                common.logger.debug(f'Docker health check passed for container ID: {self.__container_id}')
            else:
                common.logger.debug(f'Docker health check failed for container ID: {self.__container_id}')
            return passed
        except (urllib.error.URLError, ConnectionResetError):
            return False
