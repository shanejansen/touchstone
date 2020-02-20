from pyfiglet import figlet_format

from touchstone import common
from touchstone.bootstrap import Bootstrap


def execute():
    common.prep_run()
    bootstrap = Bootstrap()
    print(figlet_format('Touchstone', font='larry3d'))

    try:
        mock_run_contexts = bootstrap.mocks.start()
        bootstrap.services.start(mock_run_contexts)
        bootstrap.mocks.services_became_available()
        tests_did_pass = bootstrap.services.run_all_tests()
        if tests_did_pass:
            print('All Touchstone tests passed successfully!')
        else:
            print('One or more Touchstone tests failed.')

        bootstrap.services.stop()
        bootstrap.mocks.stop()
        bootstrap.runner.exit_touchstone(tests_did_pass)
    except (Exception, KeyboardInterrupt) as e:
        print('\nTouchstone was interrupted. Cleaning up...')
        bootstrap.runner.cleanup()
        raise e
