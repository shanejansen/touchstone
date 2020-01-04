from pyfiglet import figlet_format

from touchstone.bootstrap import Bootstrap


def execute():
    bootstrap = Bootstrap()
    bootstrap.touchstone_config.set_dev()
    bootstrap.runner.prep_run()
    print(figlet_format('Touchstone', font='larry3d'))

    try:
        bootstrap.mocks.start()
        bootstrap.mocks.load_defaults()
        bootstrap.mocks.print_available_mocks()

        __print_help()
        while True:
            command = input('Touchstone Command: ')
            if command == 'help':
                __print_help()
            elif command == 'run':
                __run_tests(bootstrap)
            elif command == 'services start':
                bootstrap.services.start()
            elif command == 'services stop':
                bootstrap.services.stop()
            elif command == 'mocks print':
                bootstrap.mocks.print_available_mocks()
            elif command == 'mocks reset':
                bootstrap.mocks.reset()
                bootstrap.mocks.load_defaults()
            elif command == 'exit':
                bootstrap.services.stop()
                bootstrap.mocks.stop()
                bootstrap.runner.exit_touchstone(True)
            else:
                print(f'Unknown command "{command}"')
    except (Exception, KeyboardInterrupt) as e:
        print('\nTouchstone was interrupted. Cleaning up...')
        bootstrap.runner.cleanup()
        raise e


def __print_help():
    print('\nDevelopment mode:\n'
          'help - Prints this message.\n'
          'run - Runs all Touchstone tests.\n'
          'services start - Starts all services under test.\n'
          'services stop - Stops all services under test.\n'
          'mocks print - Prints mock UI URLs.\n'
          'mocks reset - Resets all mocks to their default state.\n'
          'exit - Exit Touchstone.\n')


def __run_tests(bootstrap):
    bootstrap.mocks.reset()
    bootstrap.mocks.load_defaults()
    tests_did_pass = bootstrap.services.run_tests()
    if tests_did_pass:
        print('All Touchstone tests passed successfully!')
    else:
        print('One or more Touchstone tests failed.')
    bootstrap.mocks.reset()
    bootstrap.mocks.load_defaults()
