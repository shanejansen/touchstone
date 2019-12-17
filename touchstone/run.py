from pyfiglet import figlet_format

from touchstone import common
from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.mocks import Mocks
from touchstone.lib.services import Services


def execute():
    try:
        common.prep_run()
        print(figlet_format('Touchstone', font='larry3d'))
        mocks = Mocks()
        mocks.start()
        mocks.load_defaults()
        services = Services(mocks)
        services.start()
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
