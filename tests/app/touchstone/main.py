import os

from app.touchstone.tests.some_test import SomeTest
from config import Config
from service import Service
from touchstone import Touchstone

root = os.path.abspath(os.path.dirname(__file__))

touchstone = Touchstone([
    Service(
        config=Config(
            service_exposed_port=8080,
            service_dockerfile=os.path.join(root, '..')
        ),
        touchstone_tests=[
            SomeTest()
        ])
], root=root)
touchstone.run()
