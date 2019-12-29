import time
import urllib.request

from touchstone.lib.touchstone_test import TouchstoneTest


class UserController(TouchstoneTest):
    def given(self):
        pass  # TODO

    def when(self):
        request = urllib.request.Request(f'{self.service_url}/user/1', method='DELETE')
        urllib.request.urlopen(request)

    def then(self, test_result) -> bool:
        time.sleep(0.5)
        return self.mocks.rabbit_mq.verify.messages_published('user.direct.exchange', routing_key='user-deleted')
