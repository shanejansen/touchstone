import os

from config import Config
from first.touchstone.tests.some_test import SomeTest
from service import Service
from touchstone import Touchstone

touchstone = Touchstone([
    Service(
        config=Config(
            service_dockerfile=os.path.abspath('../')
        ),
        touchstone_tests=[
            SomeTest()
        ])
])
touchstone.run()
