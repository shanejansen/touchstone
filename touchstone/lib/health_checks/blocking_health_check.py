import time

from touchstone.lib.health_checks.i_health_checkable import IHealthCheckable


class BlockingHealthCheck(object):
    def __init__(self, seconds_between_retries: int, num_retries: int, target: IHealthCheckable):
        self.__seconds_between_retries = seconds_between_retries
        self.__num_retries = num_retries
        self.__target = target

    def wait_until_healthy(self) -> bool:
        for retry_num in range(self.__num_retries):
            if self.__target.is_healthy():
                return True
            else:
                time.sleep(self.__seconds_between_retries)
        return False
