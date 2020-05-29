from pyfiglet import figlet_format

from touchstone import common
from touchstone.bootstrap import Bootstrap


def execute():
    if not common.sanity_check_passes():
        exit(1)
    bootstrap = Bootstrap()
    print(figlet_format('Touchstone', font='larry3d'))

    try:
        bootstrap.mocks.start()
        bootstrap.services.start(bootstrap.mocks.environment_vars())
        bootstrap.mocks.services_became_available()
        tests_did_pass = bootstrap.services.run_all_tests()
        if tests_did_pass:
            print('All Touchstone tests passed successfully!')
        else:
            print('One or more Touchstone tests failed.')
        bootstrap.exit(tests_did_pass)
    except (Exception, KeyboardInterrupt) as e:
        print('\nTouchstone was interrupted. Cleaning up...')
        bootstrap.cleanup()
        raise e
