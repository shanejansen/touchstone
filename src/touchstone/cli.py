import logging
import os

import click

from touchstone import common
from touchstone import develop
from touchstone import init
from touchstone import run
from touchstone.lib import exceptions
from touchstone.lib.configs.touchstone_config import TouchstoneConfig


@click.group()
@click.option('--log', default='WARNING', help='Sets the log level.')
def cli(log):
    TouchstoneConfig.instance().set_root(os.getcwd())
    numeric_level = getattr(logging, log.upper(), None)
    if not isinstance(numeric_level, int):
        raise exceptions.TouchstoneException(f'Invalid log level: {log}')
    logging.basicConfig()
    common.logger.setLevel(numeric_level)


@cli.command(name='init', help='Initialize Touchstone in the current directory.')
def init_cmd():
    init.execute()


@cli.command(name='run', help='Run Touchstone and exit.')
def run_cmd():
    run.execute()


@cli.command(name='develop', help='Start a development session of Touchstone.')
def develop_cmd():
    develop.execute()


if __name__ == '__main__':
    cli()
