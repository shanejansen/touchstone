import json
import os
import sys

import click
from pyfiglet import figlet_format

from configs.touchstone_config import TouchstoneConfig
from docker_manager import DockerManager
from mocks.mocks import Mocks
from services import Services


@click.group()
def cli():
    pass


@cli.command()
def init():
    # create touchstone.json if not exists
    # create dev-defaults if not exists
    pass


@cli.command()
def run():
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
        exit_touchstone(tests_did_pass)
    except (Exception, KeyboardInterrupt) as e:
        print('\nTouchstone was interrupted. Cleaning up...')
        DockerManager.instance().cleanup()
        raise e


@cli.command()
def develop():
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
                load_config()
                tests_did_pass = services.run_tests()
                if tests_did_pass:
                    print('All Touchstone tests passed successfully!')
                else:
                    print('One or more Touchstone tests failed.')
                mocks.load_defaults()
            elif command == 'exit':
                exit_touchstone(True)
            else:
                print(f'Unknown command "{command}"')
    except (Exception, KeyboardInterrupt) as e:
        print('\nTouchstone was interrupted. Cleaning up...')
        DockerManager.instance().cleanup()
        raise e


def load_config():
    path = os.path.join(TouchstoneConfig.instance().config['root'], 'touchstone.json')
    with open(path, 'r') as file:
        TouchstoneConfig.instance().merge(json.load(file))
        # TODO: Re-merge touchstone_config in dev mode re-run


def sanity_check():
    path = os.path.join(TouchstoneConfig.instance().config['root'], 'touchstone.json')
    if not os.path.exists(path):
        print('touchstone.json could not be found. If touchstone has not been initialized, run \'touchstone init\'.')
        exit(1)


def exit_touchstone(did_pass: bool):
    print('Exiting...')
    if did_pass:
        code = 0
    else:
        code = 1
    DockerManager.instance().cleanup()
    sys.exit(code)


TouchstoneConfig.instance().set_root(os.getcwd())
sanity_check()
load_config()
cli()
