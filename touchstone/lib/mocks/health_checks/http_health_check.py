import urllib.error
import urllib.request

from touchstone.lib import exceptions
from touchstone.lib.mocks.health_checks.i_url_health_checkable import IUrlHealthCheckable


class HttpHealthCheck(IUrlHealthCheckable):
    def __init__(self):
        self.__url = None

    def set_url(self, url: str):
        self.__url = url

    def is_healthy(self) -> bool:
        if not self.__url:
            raise exceptions.MockException('URL must be set before checking health.')
        try:
            response = urllib.request.urlopen(self.__url).read()
            return False if response is None else True
        except (urllib.error.URLError, ConnectionResetError):
            return False
