from pyfiglet import figlet_format

from commands import common
from configs.touchstone_config import TouchstoneConfig
from docker_manager import DockerManager
from mocks.mocks import Mocks
from services import Services


def execute():
    try:
        print(figlet_format('Touchstone', font='larry3d'))
        TouchstoneConfig.instance().set_dev()
        mocks = Mocks()
        mocks.start()
        mocks.load_defaults()
        mocks.print_available_mocks()
        services = Services(mocks)
        print('\nIn dev mode - keeping alive\n'
              'run - Runs all Touchstone tests.\n'
              'exit - Exit Touchstone.')
        while True:
            command = input('Touchstone Command: ')
            if command == 'run':
                common.load_config()
                tests_did_pass = services.run_tests()
                if tests_did_pass:
                    print('All Touchstone tests passed successfully!')
                else:
                    print('One or more Touchstone tests failed.')
                mocks.load_defaults()
            elif command == 'exit':
                common.exit_touchstone(True)
            else:
                print(f'Unknown command "{command}"')
    except (Exception, KeyboardInterrupt) as e:
        print('\nTouchstone was interrupted. Cleaning up...')
        DockerManager.instance().cleanup()
        raise e
