from pyfiglet import figlet_format

from commands import common
from docker_manager import DockerManager
from mocks.mocks import Mocks
from services import Services


def execute():
    try:
        print(figlet_format('Touchstone', font='larry3d'))
        mocks = Mocks()
        mocks.start()
        services = Services(mocks)
        tests_did_pass = services.run_tests()
        if tests_did_pass:
            print('All Touchstone tests passed successfully!')
        else:
            print('One or more Touchstone tests failed.')
        common.exit_touchstone(tests_did_pass)
    except (Exception, KeyboardInterrupt) as e:
        print('\nTouchstone was interrupted. Cleaning up...')
        DockerManager.instance().cleanup()
        raise e
