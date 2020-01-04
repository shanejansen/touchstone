from pyfiglet import figlet_format

from touchstone.bootstrap import Bootstrap


def execute():
    bootstrap = Bootstrap()
    bootstrap.runner.prep_run()
    print(figlet_format('Touchstone', font='larry3d'))

    try:
        bootstrap.mocks.start()
        bootstrap.mocks.load_defaults()

        bootstrap.services.start()
        tests_did_pass = bootstrap.services.run_tests()
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
