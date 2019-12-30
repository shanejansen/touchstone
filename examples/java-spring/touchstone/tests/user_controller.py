import urllib.request

from touchstone.lib.touchstone_test import TouchstoneTest


class DeleteUser(TouchstoneTest):
    def processing_period(self) -> float:
        return 0.5

    def given(self):
        pass  # TODO

    def when(self):
        request = urllib.request.Request(f'{self.service_url}/user/1', method='DELETE')
        urllib.request.urlopen(request)

    def then(self, test_result) -> bool:
        return self.mocks.rabbit_mq.verify.payload_published('user.exchange', '1', routing_key='user-deleted')
