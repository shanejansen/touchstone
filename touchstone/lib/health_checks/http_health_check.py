import urllib.error
import urllib.request

from touchstone import common
from touchstone.lib import exceptions
from touchstone.lib.health_checks.i_health_checkable import IHealthCheckable


class HttpHealthCheck(IHealthCheckable):
    def __init__(self):
        self.__url = None

    def set_url(self, url: str):
        self.__url = url

    def is_healthy(self) -> bool:
        if not self.__url:
            raise exceptions.MockException('URL must be set before checking health.')
        try:
            common.logger.debug(f'Executing HTTP health check for: {self.__url}')
            code = urllib.request.urlopen(self.__url).getcode()
            passed = code % 200 < 100
            if passed:
                common.logger.debug(f'HTTP health check passed for: {self.__url}')
            else:
                common.logger.debug(f'HTTP health check failed for: {self.__url}')
            return passed
        except (urllib.error.URLError, ConnectionResetError):
            return False
