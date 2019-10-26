import http.server
import socketserver
import threading
import time

from config import Config
from test_group import TestGroup
from touchstone import Touchstone
from touchstone_test import TouchstoneTest


def serve_http():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(('', 8080), handler) as httpd:
        print('HTTP available on port 8080.')
        httpd.serve_forever()


def run_test():
    touchstone = Touchstone([
        TestGroup(
            config=Config(
                service_port=8080,
                service_host='localhost',
            ),
            touchstone_tests=[
                SomeTest()
            ])
    ])
    touchstone.run()


class SomeTest(TouchstoneTest):
    def name(self):
        return 'Some Test'

    def given(self, given_context):
        pass

    def when(self, when_context):
        return 1

    def then(self, then_context, test_result):
        return test_result == 1


threading.Thread(target=serve_http, daemon=True).start()
time.sleep(2)
run_test()
