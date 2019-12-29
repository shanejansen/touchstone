import time

from touchstone.lib.touchstone_test import TouchstoneTest


class Test(object):
    def __init__(self, name: str, touchstone_test: TouchstoneTest):
        self.name = name
        self.__touchstone_test = touchstone_test

    def run(self) -> bool:
        self.__touchstone_test.given()
        result = self.__touchstone_test.when()
        time.sleep(self.__touchstone_test.processing_period())
        did_pass = self.__touchstone_test.then(result)
        return did_pass
