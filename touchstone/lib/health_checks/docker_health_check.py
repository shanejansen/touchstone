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
            command = f'docker inspect {{TODO}} {self.__container_id}'
            passed = subprocess.run(command, shell=True) == 'success'
            if passed:
                common.logger.debug(f'Docker health check passed for container ID: {self.__container_id}')
            else:
                common.logger.debug(f'Docker health check failed for container ID: {self.__container_id}')
            return passed
        except (urllib.error.URLError, ConnectionResetError):
            return False
