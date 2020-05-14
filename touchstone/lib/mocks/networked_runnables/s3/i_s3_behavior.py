import abc

from touchstone.lib.mocks.networked_runnables.s3.s3_setup import S3Setup
from touchstone.lib.mocks.networked_runnables.s3.s3_verify import S3Verify


class IS3Behavior(object):
    @abc.abstractmethod
    def setup(self) -> S3Setup:
        pass

    @abc.abstractmethod
    def verify(self) -> S3Verify:
        pass
