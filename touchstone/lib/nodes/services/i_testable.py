import abc


class ITestable(object):
    @abc.abstractmethod
    def run_test(self, file_name, test_name) -> bool:
        pass

    @abc.abstractmethod
    def run_all_tests(self) -> bool:
        pass
