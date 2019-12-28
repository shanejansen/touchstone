from pyfiglet import figlet_format

from touchstone import common
from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.mocks import Mocks
from touchstone.lib.services import Services


def execute():
    try:
        common.prep_run()
        print(figlet_format('Touchstone', font='larry3d'))
        TouchstoneConfig.instance().set_dev()

        mocks = Mocks()
        mocks.start()
        mocks.load_defaults()
        mocks.print_available_mocks()

        services = Services(mocks)

        __print_help()
        while True:
            command = input('Touchstone Command: ')
            if command == 'help':
                __print_help()
            elif command == 'run':
                __run_tests(mocks, services)
            elif command == 'services start':
                services.start()
            elif command == 'services stop':
                services.stop()
            elif command == 'mocks print':
                mocks.print_available_mocks()
            elif command == 'mocks reset':
                mocks.reset()
                mocks.load_defaults()
            elif command == 'exit':
                services.stop()
                mocks.stop()
                common.exit_touchstone(True)
            else:
                print(f'Unknown command "{command}"')
    except (Exception, KeyboardInterrupt) as e:
        print('\nTouchstone was interrupted. Cleaning up...')
        DockerManager.instance().cleanup()
        raise e


def __print_help():
    print('\nDevelopment mode:\n'
          'help - Prints this message.\n'
          'run - Runs all Touchstone tests.\n'
          'services start - Starts all services under test. Services will be re-started if already running.\n'
          'services stop - Stops all services under test.\n'
          'mocks print - Prints mock UI URLs.\n'
          'mocks reset - Resets all mocks to their default state.\n'
          'exit - Exit Touchstone.\n')


def __run_tests(mocks, services):
    mocks.reset()
    mocks.load_defaults()
    common.load_config()
    tests_did_pass = services.run_tests()
    if tests_did_pass:
        print('All Touchstone tests passed successfully!')
    else:
        print('One or more Touchstone tests failed.')
    mocks.reset()
    mocks.load_defaults()
